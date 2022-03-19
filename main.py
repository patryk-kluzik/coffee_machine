from data import MENU, resources

resources["money"] = 0

# TODO: 1) Prompt user by asking “What would you like? (espresso/latte/cappuccino):”
#  a. Check the user’s input to decide what to do next.
#  b. The prompt should show every time action has completed, e.g. once the drink is
#  dispensed. The prompt should show again to serve the next customer

# TODO 2) Turn off the Coffee Machine by entering “off” to the prompt.
#  a. For maintainers of the coffee machine, they can use “off” as the secret word
#  to turn off the machine. Your code should end execution when this happens.

# TODO 3) Print report.
#  a. When the user enters “report” to the prompt, a report should be generated that shows
#  the current resource values. e.g.Water: 100m Milk: 50ml Coffee: 76g Money: $2.5


def format_report(coffee_resources):
    """

    This function takes the resources as the parameter and returns a string of formatted
    text which will be printed to the console

    :param coffee_resources a dictionary of all coffees
    :return: formatted string of all resources and their values
    """
    # list of all the keys
    keys = list(coffee_resources.keys())
    return f"{keys[0]}: {coffee_resources[keys[0]]} \n" \
           f"{keys[1]}: {coffee_resources[keys[1]]} \n" \
           f"{keys[2]}: {coffee_resources[keys[2]]} \n" \
           f"{keys[3]}: ${coffee_resources[keys[3]]}"


# TODO 4) Check resources sufficient?
#  a. When the user chooses a drink, the program should check if there are enough  resources to make that drink.
#  b. E.g. if Latte requires 200ml water but there is only 100ml left in the machine.
#  It should not continue to make the drink but print: “Sorry there is not enough water.”
#  c. The same should happen if another resource is depleted, e.g. milk or coffee.

def enough_resources(coffee_choice):
    """

    This function takes the dictionary of coffee as param, with the ingredients and the cost
    and checks if there are enough resources to make the coffee by comparing the values for the keys between
    the coffee dictionary and the resources dictionary and returns a list of bools

    :param coffee_choice: return dictionary of the coffee chosen my user
    :return: list of bools, adding True if there are enough resources to make coffee otherwise False
    """
    not_enough_of = []
    for i in coffee_choice["ingredients"]:
        # coffee require more resources than there are resources
        if coffee_choice["ingredients"][i] > resources[i]:
            not_enough_of.append(i)

    return not_enough_of


def print_missing_resources(missing_resources_list):
    """
    Function takes a list of missing resources returned from enough_resources() and
    returns formatted string of the resources concat with " or " for more than 1 resource missing
    or simply returns the string of the resource

    :param missing_resources_list:
    :return: resources as a formatted string
    """
    missing_resources_local_str = ''
    for i in missing_resources_list:
        if i != missing_resources_list[-1]:
            missing_resources_local_str += i + " or "
        else:
            missing_resources_local_str += i
    return missing_resources_local_str


# TODO 5) Process coins.
#  a. If there are sufficient resources to make the drink selected, then the program should
#  prompt the user to insert coins.
#  b. Remember that quarters = $0.25, dimes = $0.10, nickles = $0.05, pennies = $0.01 c. Calculate the monetary value
#  of the coins inserted. E.g. 1 quarter, 2 dimes, 1 nickel, 2 pennies = 0.25 + 0.1 x 2 + 0.05 + 0.01 x 2 = $0.52

def process_coins(coffee_choice):
    """

    Function takes the dictionary of the users choice of coffee which will use "cost" key to determine price.
    Then the use will insert coins, and we will return the remaining change.

    :param coffee_choice: dictionary containing information on chosen coffee
    :return: list with a bool (to determine if enough money was put in) and float of money returned
    """

    coffee_price = coffee_choice["cost"]

    quarters = int(input("How many quarters?: ")) * 0.25
    dimes = int(input("How many dimes?: ")) * 0.10
    nickels = int(input("How many nickels?: ")) * 0.05
    pennies = int(input("How many pennies?: ")) * 0.01

    money_inserted = quarters + dimes + nickels + pennies

    if money_inserted >= coffee_price:
        money_refunded = money_inserted - coffee_price
    else:
        money_refunded = money_inserted

    output = [money_inserted >= coffee_price, round(money_refunded, 2)]

    return output


# TODO 7) Make Coffee.
#  a. If the transaction is successful and there are enough resources to make the drink the
#  user selected, then the ingredients to make the drink should be deducted from the coffee machine resources.
#  E.g. report before purchasing latte:
#       Water: 300ml
#       Milk: 200ml
#       Coffee: 100g
#       Money: $0
#  Report after purchasing latte:
#       Water: 100ml
#       Milk: 50ml
#       Coffee: 76g
#       Money: $2.5
#  b. Once all resources have been deducted, tell the user “Here is your latte. Enjoy!” or their choice of drink.


def make_coffee(coffee_choice, refund_money):
    """

    Function takes a dictionary (coffee_choice) and assigns a new variable "ingredients_to_deduct" dictionary values of
    the "ingredients" key. Local scope variable "updated_resources" references the "resources" dictionary. A for loop
    then loops through all keys associated with "ingredients" key - the updated_resources dict is then updated for each
    key by subtracting the values of the updated_resources key from the "ingredients_to_deduct" - therefore updating the
    outer-scope variable that is "resources". Then print the refund amount and coffee choice.

    :param coffee_choice: dict containing values of the user chosen coffee
    :param refund_money: float of the money refunded
    """
    ingredients_to_deduct = coffee_choice["ingredients"]
    updated_resources = resources

    for i in coffee_choice["ingredients"]:
        updated_resources[i] = updated_resources[i] - ingredients_to_deduct[i]

    print(f"Here is ${refund_money[1]} in change.")
    print(f"Here is your {choice_str}. Enjoy!")


coffee_machine_on = True

while coffee_machine_on:
    choice_str = input(f"What would you like? (espresso/latte/cappuccino):").lower()
    if choice_str in MENU:
        choice_dict = MENU[choice_str]
        missing_resources = enough_resources(choice_dict)
        if missing_resources:
            missing_resources_str = print_missing_resources(missing_resources)
            print(f"Sorry, there isn't enough {missing_resources_str}.")
        else:
            # TODO 6) Check transaction successful?
            #  a. Check that the user has inserted enough money to purchase the drink they selected.
            #  E.g Latte cost $2.50, but they only inserted $0.52 then after counting the coins the
            #  program should say “Sorry that's not enough money. Money refunded.”.
            #  b. But if the user has inserted enough money, then the cost of the drink gets added to the
            #  machine as the profit and this will be reflected the next time “report” is triggered. E.g.
            #  Water: 100ml
            #  Milk: 50ml
            #  Coffee: 76g
            #  Money: $2.5
            #  c. If the user has inserted too much money, the machine should offer change.
            #  E.g. “Here is $2.45 dollars in change.” The change should be rounded to 2 decimal places.
            refund = process_coins(choice_dict)
            # if first element of the list is True - enough money was inserted
            if refund[0]:
                resources["money"] += choice_dict["cost"]
                make_coffee(choice_dict, refund)
            else:
                print(f"Sorry, insufficient funds. Refunded ${refund[1]}.")

    elif choice_str == 'off':
        print("Switching off for maintenance")
        coffee_machine_on = False
    elif choice_str == 'report':
        print(format_report(resources))
    else:
        print("Invalid options, try again!")
