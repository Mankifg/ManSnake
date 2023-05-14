import random
import typing

matching_moves = {
    "u":"up",
    "d":"down",
    "l":"left",
    "r":"right",
}


def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Mankifg",  
        "color": "#FF0000", 
        "head": "beluga",
        "tail": "default",  
    }


def start(game_state: typing.Dict):
    print("GAME START")

def end(game_state: typing.Dict):
    print("GAME OVER\n")

def new_x_y(direction,x,y):
    if direction == "u":
        return x,y+1
    elif direction == "d":
        return x,y-1
    elif direction == "l":
        return x-1,y
    elif direction == "r":
        return x+1,y
    else:
        print("Errorrrr")
        return x,y


def avoid_wall(moves,px,py,bx,by):
    for m in moves:
        nx,ny = new_x_y(m,px,py)
        if (nx == bx or nx == -1) or (ny == by or ny == -1):
            moves = moves.remove(m)

    return moves
            

def dont_move_self(moves,game_state):
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        moves = moves.remove("l")

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        moves = moves.remove("r")
        
    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        moves = moves.remove("d")

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        moves = moves.remove("up")
        

    return moves

def bad_positions(gs):
    pos = []

    you_body = gs["you"]["body"]

    for body_peace in you_body:
        x,y = body_peace["x"], body_peace["y"]
        pos.append((x,y))
    other_snakes = gs["board"]["snakes"]

    for x_snake in other_snakes:
        x_snake_body = x_snake["body"]
        for body_peace in x_snake_body:
            x,y = body_peace["x"],body_peace["y"]
            pos.append((x,y))

    print(pos)
    return pos

def avoid_bad_pos(gs,possible_moves,px,py):
    bad_pos = bad_positions(gs)
    for m in possible_moves:
        nx,ny = new_x_y(m,px,py)
        if (nx,ny) in bad_pos:
            possible_moves.remove(m)
            
    return possible_moves



def move(game_state: typing.Dict) -> typing.Dict:

    possible_moves = ["u","d","l","r"]

    possible_moves = dont_move_self(possible_moves,game_state)

    head = game_state["you"]["body"][0]
    px = head["x"]
    py = head["y"]

    
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']  
    
    possible_moves = avoid_wall(possible_moves,px,py,board_width,board_height)
    possible_moves = avoid_bad_pos(game_state,possible_moves,px,py)



    print(len(possible_moves))
    
    if len(possible_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving up")
        return {"move": "up"}

    next_move = random.choice(possible_moves)
    next_move = matching_moves[next_move]

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server
  
    run_server({"info": info, "start": start, "move": move, "end": end})