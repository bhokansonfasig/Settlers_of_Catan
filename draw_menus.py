from tkinter import *

def draw_log(app):
    """Adds log to board window"""
    app.displays.log_text = Text(app.board_canvas, height=2, width=30,
        background=app.style.background_color,
        font=(app.style.txt_font,int(app.style.txt_size*.8)))
    app.displays.log_text_window = app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)/2),
        int(app.style.win_height*7/8),
        height=int(app.style.win_height/4),
        width=app.style.hex_x_off-app.style.water_width,
        window=app.displays.log_text, tags="log")
    app.pieces.log_file = open(app.pieces.log_file_name,'a+')
    app.pieces.log_file.seek(0)
    fullfile = app.pieces.log_file.read()
    app.displays.log_text.insert(END, fullfile)
    app.displays.log_text.config(state=DISABLED)


def undraw_log(app):
    """Undraws log from the board window"""
    app.board_canvas.delete("log")
    app.displays.log_text.destroy()
    app.pieces.log_file.close()


def write_log(app,text,*args,sep=" ",end="\n"):
    """Writes text to the log"""
    write_text = str(text)
    for arg in args:
        write_text += sep
        write_text += str(arg)
    write_text += end
    app.displays.log_text.config(state=NORMAL)
    app.displays.log_text.insert(END, write_text)
    app.displays.log_text.yview(MOVETO, 1)
    app.displays.log_text.config(state=DISABLED)
    app.pieces.log_file.write(write_text)


def draw_status_box(app):
    """Draws a status box indicating what's going on right now"""
    app.board_canvas.delete("status")

    border_width = int(.2*app.style.txt_size)
    app.board_canvas.create_rectangle(
        int((app.style.hex_x_off-app.style.water_width)*3/5),
        0,#int((app.style.hex_y_off-app.style.water_width)*1/20),
        int(app.style.hex_x_off-app.style.water_width)-border_width,
        int(app.style.hex_y_off-app.style.water_width)-border_width,
        outline='white', width=border_width, tags="status")

    if app.pieces.phase_index()<3:
        status_text = "Setting up game"
    else:
        active_player = app.pieces.players[app.pieces.active_index].name
        if app.pieces.turn_phase=="first placements":
            action = "is choosing initial position"
        elif app.pieces.turn_phase=="second placements":
            action = "is choosing second position"
        elif app.pieces.turn_phase=="roll dice":
            action = "is rolling the dice"
        elif app.pieces.turn_phase=="discard":
            action = "is getting robbed"
        elif app.pieces.turn_phase=="place robber":
            action = "is placing the robber"
        elif app.pieces.turn_phase=="end game":
            action = "has won!"
        else:
            action = "is thinking carefully"
        status_text = active_player+" "+action

    app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*4/5),
        int((app.style.hex_y_off-app.style.water_width)*10/20),
        text=status_text, font=(app.style.txt_font,int(app.style.txt_size)),
        width=int((app.style.hex_x_off-app.style.water_width)*2/5)-4*border_width,
        justify=CENTER, tags="status")


def trade_menu(player,app):
    """Clears buttons and draws trading screen for player"""
    from catan_logic import perform_trade, evaluate_port_trade

    undraw_buttons(app)


    port_give_text = StringVar()
    port_get_text = StringVar()
    port_give_text.set("4 wood")
    port_get_text.set("1 brick")
    port_give_entry = Entry(app.board_canvas, width=8,
        textvariable=port_give_text)
    port_give_window = app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*3/10),
        int(app.style.win_height*.4+2*app.style.txt_size),
        window=port_give_entry, tags="trade")
    port_get_entry = Entry(app.board_canvas, width=8,
        textvariable=port_get_text)
    port_get_window = app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*7/10),
        int(app.style.win_height*.4+2*app.style.txt_size),
        window=port_get_entry, tags="trade")

    port_trade_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="Request Port Trade",
        command=lambda : app.set_button_chosen(1))
    port_trade_button.configure(width=20, height=1, padx=0, pady=0)
        #background=inactive_button_color, activebackground=active_button_color)
    port_button_window = app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*5/10),
        int(app.style.win_height*.4+4*app.style.txt_size),
        window=port_trade_button, tags="trade")


    cancel_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="Stop Trading",
        command=lambda : app.set_button_chosen(0))
    cancel_button.configure(width=15, height=1, padx=0, pady=0)
        #background=inactive_button_color, activebackground=active_button_color)
    cancel_window = app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*5/10),
        int(app.style.win_height*.4+10*app.style.txt_size),
        window=cancel_button, tags="trade")

    app.button_chosen.set(-1)
    while app.button_chosen.get()!=0:
        draw_stats(app)
        draw_resources(player,app)
        app.board_canvas.wait_variable(app.button_chosen)

        if app.button_chosen.get()==1:
            given_resource = port_give_text.get()
            gotten_resource = port_get_text.get()
            trade_successful, mul = evaluate_port_trade(given_resource,
                gotten_resource,player)
            if trade_successful:
                perform_trade(player,given_resource,gotten_resource,app,mul)

    app.button_chosen.set(-1)


    app.board_canvas.delete("trade")
    port_trade_button.destroy()

    draw_buttons(player,app)


def maritime_trade(player,app):
    """Clears buttons and draws trading screen for player"""
    from catan_logic import perform_trade

    undraw_buttons(app)

    res_give_options = []
    res_get_options = ["wood","brick","sheep","wheat","stone"]

    if "any" in player.ports or "?" in player.ports:
        trade_ratio = 3
    else:
        trade_ratio = 4

    mul = {"wood":trade_ratio,"brick":trade_ratio,"sheep":trade_ratio,"wheat":trade_ratio,"stone":trade_ratio}

    if ("wood" in player.ports) and player.wood>=2:
        res_give_options += [str(2*x)+" wood" for x in range(1,int(player.wood/2)+1)]
        mul["wood"] = 2
    elif player.wood>=trade_ratio:
        res_give_options += [str(x*trade_ratio)+" wood" for x in range(1,int(player.wood/trade_ratio)+1)]
    if ("brick" in player.ports) and player.brick>=2:
        res_give_options += [str(2*x)+"  brick" for x in range(1,int(player.brick/2)+1)]
        mul["brick"] = 2
    elif player.brick>=trade_ratio:
        res_give_options += [str(x*trade_ratio)+" brick" for x in range(1,int(player.brick/trade_ratio)+1)]
    if ("sheep" in player.ports) and player.sheep>=2:
        res_give_options += [str(2*x)+"  sheep" for x in range(1,int(player.sheep/2)+1)]
        mul["sheep"] = 2
    elif player.sheep>=trade_ratio:
        res_give_options += [str(x*trade_ratio)+" sheep" for x in range(1,int(player.sheep/trade_ratio)+1)]
    if ("wheat" in player.ports) and player.wheat>=2:
        res_give_options += [str(2*x)+" wheat" for x in range(1,int(player.wheat/2)+1)]
        mul["wheat"] = 2
    elif player.wheat>=trade_ratio:
        res_give_options += [str(x*trade_ratio)+" wheat" for x in range(1,int(player.wheat/trade_ratio)+1)]
    if ("stone" in player.ports) and player.stone>=2:
        res_give_options += [str(2*x)+" stone" for x in range(1,int(player.stone/2)+1)]
        mul["stone"] = 2
    elif player.stone>=trade_ratio:
        res_give_options += [str(x*trade_ratio)+" stone" for x in range(1,int(player.stone/trade_ratio)+1)]

    if len(res_give_options)!=0:
        res_give_text = app.board_canvas.create_text(
            int((app.style.hex_x_off-app.style.water_width)*5/10),
            int(app.style.win_height*.4), text="Trade the resources:",
            font=(app.style.txt_font,int(.8*app.style.txt_size)), tags="trade")
        res_give = StringVar()
        res_give.set("Choose a resource to give")
        res_give_menu = OptionMenu(app.board_canvas,res_give,*res_give_options)
        res_give_window = app.board_canvas.create_window(
            int((app.style.hex_x_off-app.style.water_width)*5/10),
            int(app.style.win_height*.4+2*app.style.txt_size),
            window=res_give_menu, tags="trade")
        res_get_text = app.board_canvas.create_text(
            int((app.style.hex_x_off-app.style.water_width)*5/10),
            int(app.style.win_height*.4+4*app.style.txt_size),
            text="for the resource:",
            font=(app.style.txt_font,int(.8*app.style.txt_size)), tags="trade")
        res_get = StringVar()
        res_get.set("Choose a resource to receive")
        res_get_menu = OptionMenu(app.board_canvas,res_get,*res_get_options)
        res_get_window = app.board_canvas.create_window(
            int((app.style.hex_x_off-app.style.water_width)*5/10),
            int(app.style.win_height*.4+6*app.style.txt_size),
            window=res_get_menu, tags="trade")
        trade_button = Button(app.board_canvas,
            font=(app.style.txt_font,int(.8*app.style.txt_size)), text="Trade",
            command=lambda : app.set_button_chosen(0))
        trade_button.configure(width=10, height=1, padx=0, pady=0)
            #background=inactive_button_color, activebackground=active_button_color)
        trade_button_window = app.board_canvas.create_window(
            int((app.style.hex_x_off-app.style.water_width)*5/10),
            int(app.style.win_height*.4+8*app.style.txt_size),
            window=trade_button, tags="trade")
    else:
        res_give_text = app.board_canvas.create_text(
            int((app.style.hex_x_off-app.style.water_width)*5/10),
            int(app.style.win_height*.4),
            text="Not enough resources to trade!",
            font=(app.style.txt_font,int(.8*app.style.txt_size)), tags="trade")
        trade_button = Button(app.board_canvas,
            font=(app.style.txt_font,int(.8*app.style.txt_size)), text="Cancel",
            command=lambda : app.set_button_chosen(0))
        trade_button.configure(width=10, height=1, padx=0, pady=0)
            #background=inactive_button_color, activebackground=active_button_color)
        trade_button_window = app.board_canvas.create_window(
            int((app.style.hex_x_off-app.style.water_width)*5/10),
            int(app.style.win_height*.4+8*app.style.txt_size),
            window=trade_button, tags="trade")

    while app.button_chosen.get()!=0:
        # draw_stats(players)
        # draw_resources(player)
        app.board_canvas.wait_variable(app.button_chosen)

    app.button_chosen.set(-1)

    if len(res_give_options)!=0:
        if res_give.get()!="Choose a resource to give" and \
            res_get.get()!="Choose a resource to receive":
            given_resource = res_give.get().split()[1]
            number = int(res_give.get().split()[0])
            gotten_resource = res_get.get()
            perform_trade(player,given_resource,gotten_resource,app,int(number/(mul[given_resource])))

        res_give_menu.destroy()
        res_get_menu.destroy()

    app.board_canvas.delete("trade")
    trade_button.destroy()

    draw_buttons(player,app)


def draw_intermediate_screen(player,app,reason="turn"):
    """Draws a screen with player name between turns"""
    if reason=="turn":
        text_string = player.name+" plays next"
    elif reason=="discard":
        text_string = player.name+" must discard"
    elif reason=="resume":
        text_string = player.name+" resume turn"
    else:
        text_string = "I'm lost..."
    intermediate_text_1 = app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)/2),
        int(app.style.win_height/3), text=text_string,
        font=(app.style.txt_font,int(1.5*app.style.txt_size)),
        fill=player.color, justify=CENTER,
        width=int(.9*(app.style.hex_x_off-app.style.water_width)))
    intermediate_text_2 = app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)/2),
        int(app.style.win_height/3)+2*app.style.txt_size,
        text="Click to continue",
        font=(app.style.txt_font,app.style.txt_size),
        fill= player.color, justify=CENTER,
        width=int(.9*(app.style.hex_x_off-app.style.water_width)))
    app.board_canvas.wait_variable(app.click_x)
    app.board_canvas.delete(intermediate_text_1)
    app.board_canvas.delete(intermediate_text_2)


def draw_stats(app):
    """Draws player statistics such as victory points, total resources, etc.
    to game board window"""
    app.board_canvas.delete("stats")

    portion = (app.style.win_width-app.style.hex_x_off+app.style.water_width)/\
        len(app.pieces.players)
    for i in range(len(app.pieces.players)):
        player = app.pieces.players[i]
        app.board_canvas.create_text(
            app.style.hex_x_off-app.style.water_width+int((i+.5)*portion),
            int((app.style.hex_y_off-app.style.water_width)/4),
            text=player.name, fill=player.color,
            font=(app.style.txt_font,int(.9*app.style.txt_size)), tags="stats")
        vp_string = "Victory points: "+str(player.score)
        app.board_canvas.create_text(
            app.style.hex_x_off-app.style.water_width+int((i+.5)*portion),
            int(2*(app.style.hex_y_off-app.style.water_width)/4),
            text=vp_string, fill=player.color,
            font=(app.style.txt_font,int(.7*app.style.txt_size)), tags="stats")
        resource_string = "Resources: "+str(player.wood+player.brick+ \
            player.wheat+player.sheep+player.stone)
        app.board_canvas.create_text(
            app.style.hex_x_off-app.style.water_width+int((i+.5)*portion),
            int(3*(app.style.hex_y_off-app.style.water_width)/4),
            text=resource_string, fill=player.color,
            font=(app.style.txt_font,int(.7*app.style.txt_size)), tags="stats")

    i = app.pieces.turn_index
    j = app.pieces.active_index
    if i==-1:
        i = j
    if i>-1 and i<len(app.pieces.players):
        app.board_canvas.create_rectangle(
            app.style.hex_x_off-app.style.water_width+int((i+.1)*portion),
            int((app.style.hex_y_off-app.style.water_width)/20),
            app.style.hex_x_off-app.style.water_width+int((i+.9)*portion),
            int((app.style.hex_y_off-app.style.water_width)*19/20),
            outline=app.pieces.players[i].color,
            width=int(.2*app.style.txt_size), tags="stats")
        # if i!=j:
        #     app.board_canvas.create_rectangle(
        #         app.style.hex_x_off-app.style.water_width+int((j+.2)*portion),
        #         int((app.style.hex_y_off-app.style.water_width)*2/20),
        #         app.style.hex_x_off-app.style.water_width+int((j+.8)*portion),
        #         int((app.style.hex_y_off-app.style.water_width)*18/20),
        #         outline=app.pieces.players[i].color,
        #         width=int(.2*app.style.txt_size), tags="stats")


def draw_buttons(player,app):
    """Draws buttons for player actions on the board window"""

    # Create buttons on board window
    app.build_settlement_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="Build Settlement", command=lambda : app.set_button_chosen(1))
    app.build_settlement_button.configure(width=13, height=1, padx=0, pady=0)
        #background=inactive_button_color, activebackground=active_button_color)
    build_settlement_button_window = app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*3/10),
        int(app.style.win_height*.4),
        window=app.build_settlement_button, tags="button")
    settlement_cost_text = app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*3/10),
        int(app.style.win_height*.4+1.25*app.style.txt_size),
        text="(1 wood, 1 brick, 1 sheep, 1 wheat)",
        font=(app.style.txt_font,int(.5*app.style.txt_size)), tags="button")
    app.build_road_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="Build Road", command=lambda : app.set_button_chosen(2))
    app.build_road_button.configure(width=13, height=1, padx=0, pady=0)
        #background=inactive_button_color, activebackground=active_button_color)
    build_road_button_window = app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*7/10),
        int(app.style.win_height*.4),
        window=app.build_road_button, tags="button")
    road_cost_text = app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*7/10),
        int(app.style.win_height*.4+1.25*app.style.txt_size),
        text="(1 wood, 1 brick)",
        font=(app.style.txt_font,int(.5*app.style.txt_size)), tags="button")
    app.build_city_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="Build City", command=lambda : app.set_button_chosen(3))
    app.build_city_button.configure(width=13, height=1, padx=0, pady=0)
        #background=inactive_button_color, activebackground=active_button_color)
    build_city_button_window = app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*3/10),
        int(app.style.win_height*.4+3*app.style.txt_size),
        window=app.build_city_button, tags="button")
    city_cost_text = app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*3/10),
        int(app.style.win_height*.4+4.25*app.style.txt_size),
        text="(2 wheat, 3 stone)",
        font=(app.style.txt_font,int(.5*app.style.txt_size)), tags="button")
    app.buy_dev_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="Development", command=lambda : app.set_button_chosen(4))
    app.buy_dev_button.configure(width=13, height=1, padx=0, pady=0)
        #background=inactive_button_color, activebackground=active_button_color)
    buy_dev_button_window = app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*7/10),
        int(app.style.win_height*.4+3*app.style.txt_size),
        window=app.buy_dev_button, tags="button")
    dev_cost_text = app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*7/10),
        int(app.style.win_height*.4+4.25*app.style.txt_size),
        text="(1 sheep, 1 wheat, 1 stone)",
        font=(app.style.txt_font,int(.5*app.style.txt_size)), tags="button")
    app.maritime_trade_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="Port Trade", command=lambda : app.set_button_chosen(5))
    app.maritime_trade_button.configure(width=13, height=1, padx=0, pady=0)
        #background=inactive_button_color, activebackground=active_button_color)
    maritime_trade_button_window = app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*3/10),
        int(app.style.win_height*.4+6*app.style.txt_size),
        window=app.maritime_trade_button, tags="button")
    app.trading_post_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="Player Trade", command=lambda : app.set_button_chosen(6))
    app.trading_post_button.configure(width=13, height=1, padx=0, pady=0)
        #background=inactive_button_color, activebackground=active_button_color)
    trading_post_button_window = app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*7/10),
        int(app.style.win_height*.4+6*app.style.txt_size),
        window=app.trading_post_button, tags="button")
    app.end_turn_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="End Turn", command=lambda : app.set_button_chosen(0))
    app.end_turn_button.configure(width=10, height=1, padx=0, pady=0)
        #background=inactive_button_color, activebackground=active_button_color)
    end_turn_button_window = app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*5/10),
        int(app.style.win_height*.4+8*app.style.txt_size),
        window=app.end_turn_button, tags="button")


def disable_buttons(player,app):
    """Disables buttons that a player cannot currently use"""
    from catan_logic import legal_settlement_placements, legal_road_placements

    if player.wood<1 or player.brick<1 or player.sheep<1 or player.wheat<1 or \
            len(legal_settlement_placements(player,app.pieces.players,
                app.pieces.all_points))==0 or \
            len(player.settlements)>=player.settlement_max:
        app.build_settlement_button.configure(state=DISABLED)
    else:
        app.build_settlement_button.configure(state=NORMAL)
    if player.wood<1 or player.brick<1 or \
            len(legal_road_placements(player,app.pieces.players,
                app.pieces.all_roads))==0 or \
            len(player.roads)>=player.road_max:
        app.build_road_button.configure(state=DISABLED)
    else:
        app.build_road_button.configure(state=NORMAL)
    if player.wheat<2 or player.stone<3 or \
        len(player.settlements)==0 or \
        len(player.cities)>=player.city_max:
        app.build_city_button.configure(state=DISABLED)
    else:
        app.build_city_button.configure(state=NORMAL)
    if player.sheep<1 or player.wheat<1 or player.stone<1:
        app.buy_dev_button.configure(state=DISABLED)
    else:
        app.buy_dev_button.configure(state=NORMAL)
    if len(player.settlements)>=player.settlement_max:
        app.build_settlement_button.configure(text="Max Built")
    else:
        app.build_settlement_button.configure(text="Build Settlement")
    if len(player.roads)>=player.road_max:
        app.build_road_button.configure(text="Max Built")
    else:
        app.build_road_button.configure(text="Build Road")
    if len(player.cities)>=player.city_max:
        app.build_city_button.configure(text="Max Built")
    else:
        app.build_city_button.configure(text="Build City")


def undraw_buttons(app):
    """Undraws and deletes all player action buttons from window"""
    app.board_canvas.delete("button")
    app.build_settlement_button.destroy()
    app.build_road_button.destroy()
    app.build_city_button.destroy()
    app.buy_dev_button.destroy()
    app.maritime_trade_button.destroy()
    app.trading_post_button.destroy()
    app.end_turn_button.destroy()


def draw_resources(player,app):
    """Undraws any current resources shown and draws resources of player"""
    app.board_canvas.delete("resources")

    # app.board_canvas.create_text(
    #     int((app.style.hex_x_off-app.style.water_width)/2),
    #     app.style.hex_y_off-app.style.water_width,
    #     text=player.name, fill=player.color,
    #     font=(app.style.txt_font, int(1.5*app.style.txt_size)),
    #     tags="resources")

    wood_text = "Wood: "+str(player.wood)
    brick_text = "Brick: "+str(player.brick)
    sheep_text = "Sheep: "+str(player.sheep)
    wheat_text = "Wheat: "+str(player.wheat)
    stone_text = "Stone: "+str(player.stone)

    app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)/2),
        app.style.hex_y_off-app.style.water_width+int(1.8*app.style.txt_size),
        text=wood_text,# anchor=NW,
        font=(app.style.txt_font,int(.8*app.style.txt_size)), #fill=wood_color,
        tags="resources")
    app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)/2),
        app.style.hex_y_off-app.style.water_width+int(2.9*app.style.txt_size),
        text=brick_text,# anchor=NW,
        font=(app.style.txt_font,int(.8*app.style.txt_size)), #fill=brick_color,
        tags="resources")
    app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)/2),
        app.style.hex_y_off-app.style.water_width+int(4.0*app.style.txt_size),
        text=sheep_text,# anchor=NW,
        font=(app.style.txt_font,int(.8*app.style.txt_size)), #fill=sheep_color,
        tags="resources")
    app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)/2),
        app.style.hex_y_off-app.style.water_width+int(5.1*app.style.txt_size),
        text=wheat_text,# anchor=NW,
        font=(app.style.txt_font,int(.8*app.style.txt_size)), #fill=wheat_color,
        tags="resources")
    app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)/2),
        app.style.hex_y_off-app.style.water_width+int(6.2*app.style.txt_size),
        text=stone_text,# anchor=NW,
        font=(app.style.txt_font,int(.8*app.style.txt_size)), #fill=stone_color,
        tags="resources")


def draw_resource_panel(player,app):
    """Draws resources available to player number 'index' in the resource panel
    of the board window. Also activates buttons available to player."""

    draw_buttons(player,app)
    disable_buttons(player,app)

    draw_resources(player,app)

    # # Temporary terminal actions for player
    # action = input("What would you like to do? ")
    # if action=="build settlement" or action=="bs":
    #     if legal_settlement_placements(player,players):
    #         build_settlement(player,players)
    #     else:
    #         print("Nowhere to legally build a new settlement!")
    # elif action=="build road" or action=="br":
    #     if legal_road_placements(player,players):
    #         build_road(player,players)
    #     else:
    #         print("Nowhere to legally build a new road!")
    # elif action=="build city" or action=="bc":
    #     if len(player.settlements)>0:
    #         build_city(player,players)
    #     else:
    #         print("Nowhere to legally build a new city!")
    # else:
    #     pass


def clear_resource_panel(app):
    """Clears out all resources from the resource panel of the board window.
    Also dims all button states."""
    try:
        undraw_buttons(app)
    except:
        pass
    app.board_canvas.delete("resources")


def draw_winning_screen(player,app):
    """Draws a congratulatory screen for the winning player"""
    text_string = player.name+" wins!"
    winning_text = app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)/2),
        int(app.style.win_height/3), text=text_string, justify=CENTER,
        font=(app.style.txt_font,3*app.style.txt_size), fill=player.color,
        width=int(.9*(app.style.hex_x_off-app.style.water_width)))
    app.board_canvas.wait_window(app.board_canvas)
