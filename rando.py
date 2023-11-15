import random

def secret_santa(names):
        participants = names[:]
        random.shuffle(participants)
        
        # Check if anyone is their own Secret Santa
        for i in range(len(participants)):
                if participants[i] == names[i]:
                        # If someone is their own Secret Santa, reshuffle and try again
                    return secret_santa(names)
    
        return {names[i]: participants[i] for i in range(len(names))}

# Example list of names
names_list = ["Alice", "Bob", "Charlie", "David", "Eve"]

# Assign Secret Santas
assignments = secret_santa(names_list)

# Display the assignments
for santa, recipient in assignments.items():
        print(f"{santa} is the Secret Santa for {recipient}")

