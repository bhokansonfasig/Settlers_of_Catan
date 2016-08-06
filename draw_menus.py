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


def draw_trade_screen(player,app):
    """Draws entry for the player to trade resources by port or with other
    players"""
    from catan_logic import predict_port_trade

    draw_resources(player,app)

    # Attempt to predict what the player will trade for
    fullest_resource, emptiest_resource = predict_port_trade(player,
        app.pieces.loop_index)
    if fullest_resource in player.ports:
        trade_ratio = 2
    elif "any" in player.ports or "?" in player.ports:
        trade_ratio = 3
    else:
        trade_ratio = 4

    app.displays.port_give_text.set(str(trade_ratio)+" "+fullest_resource)
    app.displays.port_get_text.set("1 "+emptiest_resource)
    port_give_entry = Entry(app.board_canvas, width=8,
        textvariable=app.displays.port_give_text)
    app.displays.add_object(port_give_entry)
    app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*3/10),
        int(app.style.win_height*.4+2*app.style.txt_size),
        window=port_give_entry, tags="trade")
    port_get_entry = Entry(app.board_canvas, width=8,
        textvariable=app.displays.port_get_text)
    app.displays.add_object(port_get_entry)
    app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*7/10),
        int(app.style.win_height*.4+2*app.style.txt_size),
        window=port_get_entry, tags="trade")

    port_trade_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="Request Port Trade",
        command=lambda : app.set_button_chosen(1))
    port_trade_button.configure(width=20, height=1, padx=0, pady=0)
        #background=inactive_button_color, activebackground=active_button_color)
    app.displays.add_object(port_trade_button)
    app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*5/10),
        int(app.style.win_height*.4+4*app.style.txt_size),
        window=port_trade_button, tags="trade")

    cancel_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="Stop Trading",
        command=lambda : app.set_button_chosen(0))
    cancel_button.configure(width=15, height=1, padx=0, pady=0)
        #background=inactive_button_color, activebackground=active_button_color)
    app.displays.add_object(cancel_button)
    app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*5/10),
        int(app.style.win_height*.4+10*app.style.txt_size),
        window=cancel_button, tags="trade")


def draw_discard_screen(player,app):
    """Draws option menus for the player to discard resources"""

    draw_resources(player,app)

    wood_discard_options = ["Wood","0"]
    brick_discard_options = ["Brick","0"]
    sheep_discard_options = ["Sheep","0"]
    wheat_discard_options = ["Wheat","0"]
    stone_discard_options = ["Stone","0"]
    for i in range(player.wood):
        wood_discard_options.append(str(i+1))
    for i in range(player.brick):
        brick_discard_options.append(str(i+1))
    for i in range(player.sheep):
        sheep_discard_options.append(str(i+1))
    for i in range(player.wheat):
        wheat_discard_options.append(str(i+1))
    for i in range(player.stone):
        stone_discard_options.append(str(i+1))

    discard_string = "Choose "+str(player.rob_count())+" resources to give up:"
    app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*5/10),
        int(app.style.win_height*.4), text=discard_string,
        font=(app.style.txt_font,int(.8*app.style.txt_size)), tags="discard")
    app.displays.wood_discard.set(wood_discard_options[0])
    wood_discard_menu = OptionMenu(app.board_canvas,app.displays.wood_discard,
        *wood_discard_options, command=lambda x: app.set_button_chosen(11))
    app.displays.add_object(wood_discard_menu)
    app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*3/10),
        int(app.style.win_height*.4+2*app.style.txt_size),
        window=wood_discard_menu, tags="discard")
    app.displays.brick_discard.set(brick_discard_options[0])
    brick_discard_menu = OptionMenu(app.board_canvas,app.displays.brick_discard,
        *brick_discard_options, command=lambda x: app.set_button_chosen(12))
    app.displays.add_object(brick_discard_menu)
    app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*7/10),
        int(app.style.win_height*.4+2*app.style.txt_size),
        window=brick_discard_menu, tags="discard")
    app.displays.sheep_discard.set(sheep_discard_options[0])
    sheep_discard_menu = OptionMenu(app.board_canvas,app.displays.sheep_discard,
        *sheep_discard_options, command=lambda x: app.set_button_chosen(13))
    app.displays.add_object(sheep_discard_menu)
    app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*3/10),
        int(app.style.win_height*.4+4*app.style.txt_size),
        window=sheep_discard_menu, tags="discard")
    app.displays.wheat_discard.set(wheat_discard_options[0])
    wheat_discard_menu = OptionMenu(app.board_canvas,app.displays.wheat_discard,
        *wheat_discard_options, command=lambda x: app.set_button_chosen(14))
    app.displays.add_object(wheat_discard_menu)
    app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*7/10),
        int(app.style.win_height*.4+4*app.style.txt_size),
        window=wheat_discard_menu, tags="discard")
    app.displays.stone_discard.set(stone_discard_options[0])
    stone_discard_menu = OptionMenu(app.board_canvas,app.displays.stone_discard,
        *stone_discard_options, command=lambda x: app.set_button_chosen(15))
    app.displays.add_object(stone_discard_menu)
    app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*3/10),
        int(app.style.win_height*.4+6*app.style.txt_size),
        window=stone_discard_menu, tags="discard")
    give_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="Give up resources", command=lambda : app.set_button_chosen(0))
    give_button.configure(width=15, height=1, padx=0, pady=0)
        #background=inactive_button_color, activebackground=active_button_color)
    app.displays.add_object(give_button)
    app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*5/10),
        int(app.style.win_height*.4+8*app.style.txt_size),
        window=give_button, tags="discard")

    total_discard_count = app.displays.get_wood_discard() + \
        app.displays.get_brick_discard() + app.displays.get_sheep_discard() + \
        app.displays.get_wheat_discard() + app.displays.get_stone_discard()
    total_string = "Total: " + str(total_discard_count)
    if total_discard_count>player.rob_count():
        total_string_color = "red"
    elif total_discard_count==player.rob_count():
        total_string_color = "#309540" #green
    else:
        total_string_color = "black"
    app.displays.total_text = app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*7/10),
        int(app.style.win_height*.4+6*app.style.txt_size),
        text=total_string, fill=total_string_color,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),tags="discard")


def draw_development_screen(player,app):
    draw_resources(player,app)

    vp_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="Reveal Victory Point Card",
        command=lambda : app.set_button_chosen(1))
    vp_button.configure(width=25, height=1, padx=0, pady=0)
    if player.development_cards["victory point"]==0:
        vp_button.configure(state=DISABLED)
        #background=inactive_button_color, activebackground=active_button_color)
    app.displays.add_object(vp_button)
    app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*5/10),
        int(app.style.win_height*.4+0*app.style.txt_size),
        window=vp_button, tags="development")

    knight_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="Use Knight Card",
        command=lambda : app.set_button_chosen(2))
    knight_button.configure(width=25, height=1, padx=0, pady=0)
    if player.development_cards["knight"]==0:
        knight_button.configure(state=DISABLED)
        #background=inactive_button_color, activebackground=active_button_color)
    app.displays.add_object(knight_button)
    app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*5/10),
        int(app.style.win_height*.4+2*app.style.txt_size),
        window=knight_button, tags="development")

    road_builder_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="Use Road Builder Card",
        command=lambda : app.set_button_chosen(3))
    road_builder_button.configure(width=25, height=1, padx=0, pady=0)
    if player.development_cards["road building"]==0:
        road_builder_button.configure(state=DISABLED)
        #background=inactive_button_color, activebackground=active_button_color)
    app.displays.add_object(road_builder_button)
    app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*5/10),
        int(app.style.win_height*.4+4*app.style.txt_size),
        window=road_builder_button, tags="development")

    plenty_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="Use Year of Plenty Card",
        command=lambda : app.set_button_chosen(4))
    plenty_button.configure(width=25, height=1, padx=0, pady=0)
    if player.development_cards["year of plenty"]==0:
        plenty_button.configure(state=DISABLED)
        #background=inactive_button_color, activebackground=active_button_color)
    app.displays.add_object(plenty_button)
    app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*5/10),
        int(app.style.win_height*.4+6*app.style.txt_size),
        window=plenty_button, tags="development")

    monopoly_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="Use Monopoly Card",
        command=lambda : app.set_button_chosen(5))
    monopoly_button.configure(width=25, height=1, padx=0, pady=0)
    if player.development_cards["monopoly"]==0:
        monopoly_button.configure(state=DISABLED)
        #background=inactive_button_color, activebackground=active_button_color)
    app.displays.add_object(monopoly_button)
    app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*5/10),
        int(app.style.win_height*.4+8*app.style.txt_size),
        window=monopoly_button, tags="development")

    cancel_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="Go Back",
        command=lambda : app.set_button_chosen(0))
    cancel_button.configure(width=10, height=1, padx=0, pady=0)
        #background=inactive_button_color, activebackground=active_button_color)
    app.displays.add_object(cancel_button)
    app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*5/10),
        int(app.style.win_height*.4+10*app.style.txt_size),
        window=cancel_button, tags="development")


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
            font=(app.style.txt_font,int(app.style.txt_size)), tags="stats")
        app.board_canvas.create_line(
            app.style.hex_x_off-app.style.water_width+int((i+.15)*portion),
            int((app.style.hex_y_off-app.style.water_width)/4 + \
                .7*app.style.txt_size),
            app.style.hex_x_off-app.style.water_width+int((i+.85)*portion),
            int((app.style.hex_y_off-app.style.water_width)/4 + \
                .7*app.style.txt_size),
            fill=player.color, tags="stats")
        app.board_canvas.create_text(
            app.style.hex_x_off-app.style.water_width+int((i+.32)*portion),
            int((app.style.hex_y_off-app.style.water_width)*7/10),
            text=str(player.score), fill=player.color,
            font=(app.style.txt_font,int(2*app.style.txt_size)), tags="stats")
        resource_string = "Res: "+str(player.resource_count())
        app.board_canvas.create_text(
            app.style.hex_x_off-app.style.water_width+int((i+.63)*portion),
            int((app.style.hex_y_off-app.style.water_width)*6/10),
            text=resource_string, fill=player.color,
            font=(app.style.txt_font,int(.7*app.style.txt_size)), tags="stats")
        development_string = "Dev: "+str(sum(player.development_cards.values()))
        app.board_canvas.create_text(
            app.style.hex_x_off-app.style.water_width+int((i+.63)*portion),
            int((app.style.hex_y_off-app.style.water_width)*8/10),
            text=development_string, fill=player.color,
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


def draw_main_screen(player,app):
    """Draws buttons for player actions on the board window and sets their
    status according to the player's resource availability."""
    from catan_logic import legal_settlement_placements, legal_road_placements

    draw_resources(player,app)

    # Create buttons on board window
    build_settlement_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="Build Settlement", command=lambda : app.set_button_chosen(1))
    build_settlement_button.configure(width=13, height=1, padx=0, pady=0)
        #background=inactive_button_color, activebackground=active_button_color)
    app.displays.add_object(build_settlement_button)
    app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*3/10),
        int(app.style.win_height*.4),
        window=build_settlement_button, tags="button")
    app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*3/10),
        int(app.style.win_height*.4+1.25*app.style.txt_size),
        text="(1 wood, 1 brick, 1 sheep, 1 wheat)",
        font=(app.style.txt_font,int(.5*app.style.txt_size)), tags="button")
    build_road_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="Build Road", command=lambda : app.set_button_chosen(2))
    build_road_button.configure(width=13, height=1, padx=0, pady=0)
        #background=inactive_button_color, activebackground=active_button_color)
    app.displays.add_object(build_road_button)
    app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*7/10),
        int(app.style.win_height*.4),
        window=build_road_button, tags="button")
    app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*7/10),
        int(app.style.win_height*.4+1.25*app.style.txt_size),
        text="(1 wood, 1 brick)",
        font=(app.style.txt_font,int(.5*app.style.txt_size)), tags="button")
    build_city_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="Build City", command=lambda : app.set_button_chosen(3))
    build_city_button.configure(width=13, height=1, padx=0, pady=0)
        #background=inactive_button_color, activebackground=active_button_color)
    app.displays.add_object(build_city_button)
    app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*3/10),
        int(app.style.win_height*.4+3*app.style.txt_size),
        window=build_city_button, tags="button")
    app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*3/10),
        int(app.style.win_height*.4+4.25*app.style.txt_size),
        text="(2 wheat, 3 stone)",
        font=(app.style.txt_font,int(.5*app.style.txt_size)), tags="button")
    buy_dev_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="Buy Dev Card", command=lambda : app.set_button_chosen(4))
    buy_dev_button.configure(width=13, height=1, padx=0, pady=0)
        #background=inactive_button_color, activebackground=active_button_color)
    app.displays.add_object(buy_dev_button)
    app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*7/10),
        int(app.style.win_height*.4+3*app.style.txt_size),
        window=buy_dev_button, tags="button")
    app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*7/10),
        int(app.style.win_height*.4+4.25*app.style.txt_size),
        text="(1 sheep, 1 wheat, 1 stone)",
        font=(app.style.txt_font,int(.5*app.style.txt_size)), tags="button")
    trade_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="Trade", command=lambda : app.set_button_chosen(5))
    trade_button.configure(width=13, height=1, padx=0, pady=0)
        #background=inactive_button_color, activebackground=active_button_color)
    app.displays.add_object(trade_button)
    app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*3/10),
        int(app.style.win_height*.4+6*app.style.txt_size),
        window=trade_button, tags="button")
    use_dev_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="Use Dev Card", command=lambda : app.set_button_chosen(6))
    use_dev_button.configure(width=13, height=1, padx=0, pady=0)
    if sum(player.development_cards.values())==0:
        use_dev_button.configure(state=DISABLED)
        #background=inactive_button_color, activebackground=active_button_color)
    app.displays.add_object(use_dev_button)
    app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*7/10),
        int(app.style.win_height*.4+6*app.style.txt_size),
        window=use_dev_button, tags="button")
    end_turn_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="End Turn", command=lambda : app.set_button_chosen(0))
    end_turn_button.configure(width=10, height=1, padx=0, pady=0)
        #background=inactive_button_color, activebackground=active_button_color)
    app.displays.add_object(end_turn_button)
    app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*5/10),
        int(app.style.win_height*.4+8*app.style.txt_size),
        window=end_turn_button, tags="button")

    # Disable unusable buttons
    if player.wood<1 or player.brick<1 or player.sheep<1 or player.wheat<1 or \
            len(legal_settlement_placements(player,app.pieces.players,
                app.pieces.all_points))==0 or \
            len(player.settlements)>=player.settlement_max:
        build_settlement_button.configure(state=DISABLED)
    # else:
    #     build_settlement_button.configure(state=NORMAL)
    if player.wood<1 or player.brick<1 or \
            len(legal_road_placements(player,app.pieces.players,
                app.pieces.all_roads))==0 or \
            len(player.roads)>=player.road_max:
        build_road_button.configure(state=DISABLED)
    # else:
    #     build_road_button.configure(state=NORMAL)
    if player.wheat<2 or player.stone<3 or \
        len(player.settlements)==0 or \
        len(player.cities)>=player.city_max:
        build_city_button.configure(state=DISABLED)
    # else:
    #     build_city_button.configure(state=NORMAL)
    if player.sheep<1 or player.wheat<1 or player.stone<1:
        buy_dev_button.configure(state=DISABLED)
    # else:
    #     buy_dev_button.configure(state=NORMAL)
    if len(player.settlements)>=player.settlement_max:
        build_settlement_button.configure(text="Max Built")
    # else:
    #     build_settlement_button.configure(text="Build Settlement")
    if len(player.roads)>=player.road_max:
        build_road_button.configure(text="Max Built")
    # else:
    #     build_road_button.configure(text="Build Road")
    if len(player.cities)>=player.city_max:
        build_city_button.configure(text="Max Built")
    # else:
    #     build_city_button.configure(text="Build City")

    # if player.dev_card_count()==0:
    #     use_dev_button.configure(state=DISABLED)



# def undraw_buttons(app):
#     """Undraws and deletes all player action buttons from window"""
#     app.board_canvas.delete("button")
#     app.build_settlement_button.destroy()
#     app.build_road_button.destroy()
#     app.build_city_button.destroy()
#     app.buy_dev_button.destroy()
#     app.maritime_trade_button.destroy()
#     app.trading_post_button.destroy()
#     app.end_turn_button.destroy()


def draw_resources(player,app):
    """Undraws any current resources shown and draws resources of player"""
    # app.board_canvas.delete("resources")

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

    vp_text = "Victory Point: "+str(player.development_cards['victory point'])
    knight_text = "Knight: "+str(player.development_cards['knight'])
    road_builder_text = "Road Builder: " + \
        str(player.development_cards['road building'])
    plenty_text = "Year of Plenty: "+str(player.development_cards['year of plenty'])
    monopoly_text = "Monopoly: "+str(player.development_cards['monopoly'])

    line_length = int((app.style.hex_x_off-app.style.water_width)*3/10)
    app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*3/10),
        app.style.hex_y_off-app.style.water_width+int(.8*app.style.txt_size),
        text="Resources",# anchor=NW,
        font=(app.style.txt_font,int(app.style.txt_size)), #fill=wood_color,
        tags="resources")
    app.board_canvas.create_line(
        int((app.style.hex_x_off-app.style.water_width)*3/10 - line_length/2),
        app.style.hex_y_off-app.style.water_width+int(1.4*app.style.txt_size),
        int((app.style.hex_x_off-app.style.water_width)*3/10 + line_length/2),
        app.style.hex_y_off-app.style.water_width+int(1.4*app.style.txt_size),
        tags="resources")
    app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*3/10),
        app.style.hex_y_off-app.style.water_width+int(2.0*app.style.txt_size),
        text=wood_text,# anchor=NW,
        font=(app.style.txt_font,int(.8*app.style.txt_size)), #fill=wood_color,
        tags="resources")
    app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*3/10),
        app.style.hex_y_off-app.style.water_width+int(3.1*app.style.txt_size),
        text=brick_text,# anchor=NW,
        font=(app.style.txt_font,int(.8*app.style.txt_size)), #fill=brick_color,
        tags="resources")
    app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*3/10),
        app.style.hex_y_off-app.style.water_width+int(4.2*app.style.txt_size),
        text=sheep_text,# anchor=NW,
        font=(app.style.txt_font,int(.8*app.style.txt_size)), #fill=sheep_color,
        tags="resources")
    app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*3/10),
        app.style.hex_y_off-app.style.water_width+int(5.3*app.style.txt_size),
        text=wheat_text,# anchor=NW,
        font=(app.style.txt_font,int(.8*app.style.txt_size)), #fill=wheat_color,
        tags="resources")
    app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*3/10),
        app.style.hex_y_off-app.style.water_width+int(6.4*app.style.txt_size),
        text=stone_text,# anchor=NW,
        font=(app.style.txt_font,int(.8*app.style.txt_size)), #fill=stone_color,
        tags="resources")

    app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*7/10),
        app.style.hex_y_off-app.style.water_width+int(.8*app.style.txt_size),
        text="Dev Cards",# anchor=NW,
        font=(app.style.txt_font,int(app.style.txt_size)), #fill=wood_color,
        tags="resources")
    app.board_canvas.create_line(
        int((app.style.hex_x_off-app.style.water_width)*7/10 - line_length/2),
        app.style.hex_y_off-app.style.water_width+int(1.4*app.style.txt_size),
        int((app.style.hex_x_off-app.style.water_width)*7/10 + line_length/2),
        app.style.hex_y_off-app.style.water_width+int(1.4*app.style.txt_size),
        tags="resources")
    app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*7/10),
        app.style.hex_y_off-app.style.water_width+int(2.0*app.style.txt_size),
        text=vp_text,# anchor=NW,
        font=(app.style.txt_font,int(.8*app.style.txt_size)), #fill=wood_color,
        tags="resources")
    app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*7/10),
        app.style.hex_y_off-app.style.water_width+int(3.1*app.style.txt_size),
        text=knight_text,# anchor=NW,
        font=(app.style.txt_font,int(.8*app.style.txt_size)), #fill=brick_color,
        tags="resources")
    app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*7/10),
        app.style.hex_y_off-app.style.water_width+int(4.2*app.style.txt_size),
        text=road_builder_text,# anchor=NW,
        font=(app.style.txt_font,int(.8*app.style.txt_size)), #fill=sheep_color,
        tags="resources")
    app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*7/10),
        app.style.hex_y_off-app.style.water_width+int(5.3*app.style.txt_size),
        text=plenty_text,# anchor=NW,
        font=(app.style.txt_font,int(.8*app.style.txt_size)), #fill=wheat_color,
        tags="resources")
    app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*7/10),
        app.style.hex_y_off-app.style.water_width+int(6.4*app.style.txt_size),
        text=monopoly_text,# anchor=NW,
        font=(app.style.txt_font,int(.8*app.style.txt_size)), #fill=stone_color,
        tags="resources")


def draw_resource_panel(player,app):
    """Draws resources available to player and other context-dependent items in
    the resource panel of the board window."""

    if app.pieces.phase_index()<=5:
        return

    if app.pieces.turn_phase=="roll dice":
        pass
    elif app.pieces.turn_phase=="discard":
        draw_discard_screen(player,app)
    elif app.pieces.turn_phase=="trade":
        draw_trade_screen(player,app)
    elif app.pieces.turn_phase=="place robber":
        draw_main_screen(player,app)
    elif app.pieces.turn_phase=="make decisions":
        draw_main_screen(player,app)
    elif app.pieces.turn_phase=="build settlement":
        draw_main_screen(player,app)
    elif app.pieces.turn_phase=="build road":
        draw_main_screen(player,app)
    elif app.pieces.turn_phase=="build city":
        draw_main_screen(player,app)
    elif app.pieces.turn_phase=="development":
        draw_development_screen(player,app)
    elif app.pieces.turn_phase=="end turn":
        pass


def clear_resource_panel(app):
    """Clears out everything from the resource panel of the board window."""

    app.board_canvas.delete("resources")
    app.board_canvas.delete("button")
    app.board_canvas.delete("trade")
    app.board_canvas.delete("discard")
    app.board_canvas.delete("development")
    app.displays.destroy_objects()


def draw_winning_screen(player,app):
    """Draws a congratulatory screen for the winning player"""
    text_string = player.name+" wins!"
    app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)/2),
        int(app.style.win_height/3), text=text_string, justify=CENTER,
        font=(app.style.txt_font,3*app.style.txt_size), fill=player.color,
        width=int(.9*(app.style.hex_x_off-app.style.water_width)))
    app.board_canvas.wait_window(app.board_canvas)
