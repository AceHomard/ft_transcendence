import requests

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise


def GetAllUniqueIds(uniqueId):
    try:
        datas = fetch_data(f"http://crypto:8020/player/get/{uniqueId}")
    except requests.exceptions.RequestException as e:
        return [], uniqueId
    result = []
    seen = set()

    for data in datas:
        for player_id in (data["player1_id"], data["player2_id"]):
            if player_id not in seen:
                result.append(player_id)
                seen.add(player_id)

    ids_string = ",".join(map(str, result))
    return datas, ids_string

def checkIfWinner(player_key, id_from_request, win_nb, data):
    if data[player_key] == data["winner_id"]:
        if data[player_key] == id_from_request:
            data["win"] = True
            win_nb["count"] += 1
        else:
            data["win"] = False


def updatePlayerData(data, player_key, unique_ids_data, id_from_request, win_nb):
    player_id = str(data[f"{player_key}_id"])
    checkIfWinner(f"{player_key}_id", id_from_request, win_nb, data)

    if player_id in unique_ids_data:
        if data[f"{player_key}_id"] == data["winner_id"]:
            data["winner_id"] = unique_ids_data[player_id]['username']
        data[f"{player_key}_img"] = unique_ids_data[player_id]["profile_picture"]
        data[f"{player_key}_pseudo"] = unique_ids_data[player_id]['username']
    else:
        data[f"{player_key}_img"] = "/media/profile_default.png"
        data[f"{player_key}_pseudo"] = "Unknown"
    data[f"{player_key}_id"] = str(data[f"{player_key}_id"])

def AddNameAndImgToDict(final_dict, unique_ids, player_id):
    unique_ids_data = fetch_data(f"http://authentification:8050/auth/user_info/{unique_ids}/")
    win_nb = {"count": 0}

    for data in final_dict:
        updatePlayerData(data, "player1", unique_ids_data, player_id, win_nb)
        updatePlayerData(data, "player2", unique_ids_data, player_id, win_nb)

    player_id_str = str(player_id)
    all_info = {
        "player_name": unique_ids_data[player_id_str]["username"] if player_id_str in unique_ids_data else "Unknown",
        "player_picture": unique_ids_data[player_id_str]["profile_picture"] if player_id_str in unique_ids_data else "/media/profile_default.png",
        "player_win": win_nb["count"],
        "player_loose": len(final_dict) - win_nb["count"],
        "player_ratio": round((win_nb["count"] / len(final_dict)) * 100) if final_dict else 0,
        "all_matchs": final_dict,
    }
    return all_info
