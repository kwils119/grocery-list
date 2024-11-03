class Recipe:
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients  # List of ingredients with quantities and measurements 

    def __str__(self):
        ingredients_list = ""
        for list in self.ingredients:
            quantity = list[0]
            measurement = list[1]
            ing = list[2]
            ingredients_list += (quantity + " " + measurement + " " + ing + "\n")
        return f"Recipe: {self.name}\n{ingredients_list}"
    
    def double_check(self):
        ingredients_list = ""
        for list in self.ingredients: 
            quantity = list[0]
            measurement = list[1]
            ing = list[2]
            ingredients_list += "Q: {quantity:10s}M: {measurement:10s}I: {ing:10s}\n".format(quantity=quantity, measurement=measurement, ing=ing)
        return(f"Recipe: {self.name}\n{ingredients_list}")
    
    def add_ingredient(self, ingredient, quantity, measurement):
        ing = [quantity, measurement, ingredient]
        self.ingredients.append(ing)
        return

def Find(name, recipes):
    for thing in recipes: 
        if name == thing.name: 
            return thing 
    print(name, "not found in recipe book.\n")
    return None 

import csv

def read_recipes_from_csv(file_path):
    recipes = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header if there is one
        current_recipe = Recipe(next(reader)[0], [])

        for row in reader:
            if current_recipe.name != row[0]:  # New recipe found
                recipes.append(current_recipe)
                current_recipe = Recipe(row[0], [])
            
            # Append ingredients to the current recipe
            quantity = row[1]
            measurement = row[2]
            ingredient = row[3]
            current_recipe.add_ingredient(ingredient=ingredient, quantity=quantity, measurement=measurement)
        
        # Don't forget to add the last recipe
        if current_recipe is not None:
            recipes.append(current_recipe)
    return recipes

# Conversion factors
conversion_factors = { #cups 
    't': 1 / 48,     
    'teaspoon': 1/48, 
    'teaspoons':1/48, 
    'T': 1 / 16,      
    'tablespoon': 1/16, 
    'tablespoons':1/16,
    'c': 1,           
    'oz': 1/2,
    'ounces':1/2,          
    'can': 2
}

# Ingredients that should not be converted
no_conversion_list = {
    'apples', 'bananas', 'tomatoes', 'carrots', 'ginger', 
    'garlic', 'chickpeas', 'fire roasted tomatoes', 'wide rice noodles', 
    'baking powder', 'biscuits', ''
}

# Specific conversion preferences
conversion_T_preferences = [
    'sugar', 
    'olive oil', 
    'curry powder', 
    'coriander', 
    'cumin', 
    'salt', 
    'sesame oil',
    'fish sauce',
    'oyster sauce', 
    'maple syrup', 
    'poultry seasoning',
    'vanilla'
]

def convert_to_measurement(quantity, measurement, ingredient):
    if ingredient.lower() in no_conversion_list:
        return quantity, measurement  # No conversion for specific ingredients
    
    # Check for specific conversion preferences
    if ingredient in conversion_T_preferences:
        if measurement in conversion_factors:
            converted_quantity = quantity * conversion_factors[measurement] / conversion_factors['T']
            return converted_quantity, 'T'

    # Default conversion to cups (c)
    if measurement in conversion_factors:
        converted_quantity = quantity * conversion_factors[measurement] / conversion_factors['c']
        return converted_quantity, 'c'

    return quantity, measurement  # If measurement is unknown, return original

def aggregate_shopping_list(recipes):
    shopping_list = {}

    for recipe in recipes:
        for item in recipe.ingredients:
            quantity, measurement, ingredient = item
            if quantity:  # Skip empty quantities
                # Convert quantity to float
                try:
                    num_quantity = eval(quantity)  # Use eval with caution; consider safer alternatives
                except Exception as e:
                    print(f"Could not convert quantity '{quantity}' for ingredient '{ingredient}': {e}")
                    continue

                # Convert to ounces, with exceptions
                (quantity_in_c, measurement) = convert_to_measurement(num_quantity, measurement, ingredient)

                if ingredient not in shopping_list:
                    shopping_list[ingredient] = [0, measurement]  # Default to c

                shopping_list[ingredient][0] += quantity_in_c

    return shopping_list

recipes = read_recipes_from_csv('recipes.csv')

print("What recipes are you making this week? Type -- when done\n")
my_recipes=[]
res = ""

while(res != "--"): 
   res = input().strip()
   if (res=="--"):
       break
   recipe = Find(res.lower(), recipes)
   if recipe != None:
      my_recipes.append(recipe)

print("These are the recipes you are making:")
for recipe in my_recipes: 
   print(recipe.double_check())
   #print(recipe)
   print("\n")
   
#shopping_list = Recipe("list", [])
shopping_list = aggregate_shopping_list(my_recipes)

print("Shopping list:")
for ingredient, (total_quantity, measurement) in shopping_list.items():
    print(f"{total_quantity:5.2f} {measurement:10s} {ingredient}")
      

