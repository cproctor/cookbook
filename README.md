# Cookbook

A simple command-line Django app for managing recipes and menus.

## Installation

    python3 -m venv env
    source env/bin/activate
    git clone https://github.com/cproctor/cookbook.git
    cd cookbook
    pip install -r requirements.txt
    ./manage.py migrate
    ./manage.py import_recipes

## Usage

Recipes are imported via YAML files storied in `recipe_sources`. 
You imported the built-in the recipes during installation with
`import_recipes`. Individual recipes can later be imported with 
`import_recipe`.

List all the recipes (add `--help` to see
options you can use to filter the view):

    ./manage.py list_recipes

    Ice Cream
    Japanese Restaurant Style Ginger Dressing
    Leek, fennel, apple & walnut soup with turmeric
    Miso Roasted Japanese Turnips
    Roasted Winter Squash and Carrots with Miso Glaze
    Wild Mushroom & Daikon Radish Cake
    ginger + lemongrass infused thai soup with crispy tofu and wild rice

New menus can be added with a management command. Let's say we are having
friends over on Thursday and we want to have turnips and ice cream.

    ./manage.py add_menu "Thursday dinner" 10 --recipes turnips "ice cream"
    ./manage.py list_menus

    Thursday dinner
    ===============
    for 10
    - 2 * Ice Cream
    - 3 * Miso Roasted Japanese Turnips

There are two main menu views: shop and cook. Again, add `--help` to see
additional options.

    ./manage.py shop thursday

    Thursday dinner
    ===============
    to serve 10
    - 2 * Ice Cream
    - 3 * Miso Roasted Japanese Turnips
    ---------------
    - 4.0 cup of cream
    - 2.0 cup of milk
    - 1.32 cup of sugar
    - 0.25 teaspoon of salt
    - 12.0 count of egg
    - 6.0 pound of turnips
    - 9.0 tablespoon of miso paste
    - 9.0 tablespoon of olive oil
    
Now a view more suitable for cooking.

    ./manage.py cook thursday
    
    Thursday dinner
    ======================================================================
    to serve 10
    - 2 * Ice Cream
    - 3 * Miso Roasted Japanese Turnips
    ----------------------------------------------------------------------
    Ingredients
    - 2 * Ice Cream
      - 4.0 cup cream (heavy)
      - 2.0 cup milk (whole)
      - 1.32 cup sugar
      - 0.25 teaspoon salt (fine sea)
      - 12.0 count egg (yolks (large))
    - 3 * Miso Roasted Japanese Turnips
      - 6.0 pound turnips (rinsed and cut in half – green parts reserved)
      - 9.0 tablespoon miso paste (white)
      - 9.0 tablespoon olive oil
    ----------------------------------------------------------------------
    Ice Cream
     - In a small pot, simmer heavy cream, milk, sugar and salt until
       sugar completely dissolves, about 5 minutes. Remove pot from heat.
       In a separate bowl, whisk yolks. Whisking constantly, slowly whisk
       about a third of the hot cream into the yolks, then whisk the yolk
       mixture back into the pot with the cream. Return pot to medium-low
       heat and gently cook until mixture is thick enough to coat the back
       of a spoon (about 170 degrees on an instant-read thermometer).
     - Strain through a fine-mesh sieve into a bowl. Cool mixture to room
       temperature. Cover and chill at least 4 hours or overnight. Churn
       in an ice cream machine according to manufacturers’ instructions.
       Serve directly from the machine for soft serve, or store in freezer
       until needed.
    ----------------------------------------------------------------------
    Miso Roasted Japanese Turnips
     - Pre-heat the oven to 425 degrees. Line a baking sheet with
       parchment paper. Set aside.
     - Whisk together the 2 tablespoons of miso paste and 2 tablespoons of
       olive oil in a bowl.
     - Spread the turnips on the prepared baking sheet. Drizzle it with
       the miso-olive oil mixture. Give it a toss to make sure that all
       turnips are coated with the mixture. Place in the oven and bake for
       12-15 minutes making sure to rotate the turnips halfway through the
       baking process. When they come out of the oven, let them cool.
       Sprinkle them with a big pinch of black pepper. Taste for seasoning
       and add in some salt if necessary.
     - Meanwhile, rinse the green parts and roughly chop them up. Heat a
       tablespoon of olive oil in a large pan. Sauté the chopped greens
       until they are lightly wilted, 2-3 minutes. Stir in the rest of the
       miso paste and make sure that the green leafs are coated with the
       paste. Add in ¼ teaspoon freshly ground black pepper. Taste for
       seasoning and add in if necessary.
     - Transfer the warm greens in a large salad bowl. Spread the roasted
       turnips on top of the greens.
     - Serve immediately.
