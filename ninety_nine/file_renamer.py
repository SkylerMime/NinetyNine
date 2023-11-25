import os

# Directory where the files are located
directory = "card_images"

# Change to the directory
os.chdir(directory)

# Mapping of card ranks to their corresponding names
rank_mapping = {
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "10": "10",
    "11": "jack",
    "12": "queen",
    "13": "king",
    "1": "ace",
}

# Mapping of card suits to their corresponding names
suit_mapping = {
    "diamond": "diamonds",
    "heart": "hearts",
    "spade": "spades",
    "club": "clubs",
}

# Iterate through each file in the directory
for suit in suit_mapping:
    os.chdir(suit)
    for filename in os.listdir("."):
        # Check if the file is a regular file
        if os.path.isfile(filename):
            # Check if the file has a valid name to be renamed
            rank = os.path.splitext(filename)[0]
            if rank in rank_mapping and os.path.splitext(filename)[1] == ".png":
                # Construct the new filename with suit and rank
                new_filename = f"{suit_mapping[suit]}_{rank_mapping[rank]}.png"

                # Rename the file
                os.rename(filename, new_filename)
                print(f"Renamed: {filename} -> {new_filename}")
            # Check if the file ends with ".svg" and delete it
            elif filename.endswith(".svg") or rank not in rank_mapping:
                os.remove(filename)
                print(f"Deleted: {filename}")
    os.chdir("..")
