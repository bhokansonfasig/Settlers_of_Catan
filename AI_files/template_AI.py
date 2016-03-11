# Template of functions needed to implement an AI for Catan

from random import choice
from point import Point
from road import Road
from tiles import Tile


def get_code():
    # Should return the AI_code for this AI
    return AI_code

def get_aliases():
    # Should return all names that initialize this AI
    return aliases


def take_turn(computer,players,available_settlement_points,
    available_roads,available_city_points):
    # Function is called to determine what action the computer should take

    # Should return "build settlement", "build road", "build city", or "ended turn"

    return action_string


def choose_settlement(computer,players,available_settlement_points):
    # Function is called to determine where the computer should place a settlement

    # Should return the point object where the settlement should be built

    return settlement


def choose_city(computer,players,available_city_points):
    # Function is called to determine where the computer should place a city

    # Should return the point object where the city should be built

    return city


def choose_road(computer,players,available_roads):
    # Function is called to determine where the computer should place a road

    # Should return the road object where the road should be built

    return road


def discard(computer,new_resource_count):
    # Function is called for computer to discard resources down to new_resource_count

    # Doesn't return anything, just needs to update the computer's resources


def place_robber(computer,tiles,original_tile):
    # Function is called to determine where the computer should place the robber tile
    #  Can't place the robber where he already is (original_tile)

    # Should return the tile object (from tiles) where the robber should be placed

    return robber_tile


def choose_target(computer,players,stealable_players):
    # Function is called to pick a player from stealable_players to take a random resource from

    # Should return the player chosen

    return target_player
