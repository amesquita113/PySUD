# This is the simple text rpg game, un-named as of yet!

from __future__ import with_statement
from __future__ import division
import os, random, time, sys, sqlite3
from io import open

# Opens the game database
conn = sqlite3.connect('./data/rpg.dat')
game_data = conn.cursor()

# Dungeon map, 0 is a room, 1 is a wall
dungeon =[[0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
          [0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
          [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
          [0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
          [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
          [1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [1, 0, 0, 1, 1, 0, 0, 0, 1, 0],
          [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
          [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
          [0, 1, 0, 0, 1, 0, 1, 0, 0, 0],
          [0, 1, 1, 1, 1, 1, 1, 0, 0, 1],
          [0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
          [1, 1, 0, 0, 1, 1, 1, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [1, 1, 0, 0, 1, 1, 0, 0, 0, 0]]

red = '\033[00;31m'
green = '\033[00;32m'
yellow = '\033[00;33m'
blue = '\033[00;34m'
magenta = '\033[00;35m'
cyan = '\033[00;36m'
white = '\033[00;37m'

def color(c):
    sys.stdout.write(c)

def leader_board():
    """ Displays the top 5 players in the game based on XP. """
    global players
    players = []
    data_file = open('./data/userdata.txt', 'r')
    for line in data_file:
        #if line.strip():
        char_stats = list(line.strip().split())
        players.append(char_stats)
    data_file.close()
    c = 0
    for line in players:
        players[c][4] = int(players[c][4])
        c += 1
    players = sorted(players, key=lambda x: x[4], reverse=True)
    c = 0
    for line in players:
        players[c][4] = unicode(players[c][4])
        c += 1
    color(blue)
    print '\nPySUD Top 5 player rankings by XP:\n'
    color(yellow)
    print ' Name              Class         Level          XP'
    color(red)
    print '=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-='
    color(yellow)
    c = 0
    for line in players:
        c += 1
        if line[1] == '1':
            line[1] = 'Fighter'
        else:
            line[1] = 'Sorcerer'
        print line[0], ' ' * (17 - len(line[0])), line[1], u' ' * (14\
              - len(line[1])), line[3], ' ' * (10 - len(line[3])), \
              line[4]
        if c == 5: break
    print ""
    pause()

    
# sample call of function : x = prompt(['1', '2', '3'], 'What would u like to do [1/2/3]:')
def prompt(l, prompt = 'Please enter your selection:',
           error='Invalid Command!'):
    """ Function to prompt the user for a selection.

    Arguments:
    list -- list of accepted inputs for the user (must be upper case)
    prompt -- the prompt that will be displayed to the user

    Returns:
    The users input once a valid input has been made.

    """
    while True:
        sys.stdout.write(white)
        ok = raw_input(prompt)
        if ok == '': ok = u'xxx'
        ok = ok.upper()        
        ok = list(ok.strip().split(None,1))
        for item in l:
            if ok[0] == item:
                return ok
        print error

# rolls to see if you encounter a enemy
def combatroll(odds=20):
    """Rolls a random 1 - 100 number and enter combat if below odds"""
    monster = random.randint(1,100)
    if monster < odds:
        ret = combat()
        return ret
        
# defines a yes/no prompt
def ask_ok(prompt='[Y/N]:', retries=5, complaint=u'Invalid selection!'):
    """Simple Yes/No prompt

    Arguments:
    prompt -- Prompt that will be displayed to the user
    retries -- The number of wrong answers before an IO Error is raised
    complaint -- What is returned when a input that is not yes/no is entered

    Returns:
    True or False based on the answer of yes or no

    """
    while True:
        ok = raw_input(prompt)
        if ok in ('y', u'ye', u'yes', u'Y', u'YE', u'YES'):
            return True
        if ok in ('n', u'no', u'N', u'NO'):
            return False
        retries = retries - 1
        if retries < 0:
            raise IOError('refusenik user')
        print 'Invalid command!'

def call_menu(menu_name):
    """Displays a text file from the ./menus/ folder."""
    menu_name = './menus/' + menu_name
    menu_file = open(menu_name, 'r')
    c = 1
    print '\n'
    for line in menu_file:
        if c == 1:
            color(magenta)
        elif c == 2:
            color(white)
        sys.stdout.write(line)
        c += 1
    menu_file.close()

# defines a "Hit enter to continue" function
def pause(unicode='Hit <Enter> to continue'):
    """Pauses untill the <Enter> key is hit"""
    color(red)
    e = (raw_input(unicode))
    
def level_up(stat_points):
    """Allows the allocation of stat points for your character.

    Arguments:
    stat_points -- The number of stat points available

    Returns:
    A value for Strength, Constitution, Dexterity and Wisdom.

    """
    color(yellow)
    print 'Congratulations, you have reached level %s!' % char_stats[3]
    const = char_stats[9]
    while stat_points > 0:
        color(white)
        print '''\nCurrent stats:
(S)trength    : %s
(D)exterity   : %s
(C)onstitution: %s
(W)isdom      : %s

You have %s points available to spend.'''%(char_stats[7], char_stats[8],
                                           char_stats[9], char_stats[10],
                                           stat_points)
        s = prompt(['S', u'D', u'C', u'W'], u'Select a stat to increase it by +1:')
        s = s[0]
        if s == 'S':
            char_stats[7] += 1
            stat_points -= 1
        if s == 'D':
            char_stats[8] += 1
            stat_points -= 1
        if s == 'C':
            char_stats[9] += 1
            stat_points -= 1
        if s == 'W':
            char_stats[10] += 1
            stat_points -= 1
    if char_stats[3] == 1:
        char_stats[6] = char_stats[6] + char_stats[9]    
    if const < char_stats[9]:
        const = char_stats[9] - const
        const = round(const/2)
        char_stats[6] = char_stats[6] + const
    if char_stats[3] > 1:
        if char_stats[1] == 1:
            char_stats[6] += 14
            game_data.execute('select * from attacks')
            for row in game_data:
                if row[4] == char_stats[3]:
                    spells.append([row[0], row[1], row[2], row[3], row[4]])
                    color(yellow)
                    print 'You have learned a new special attack!'
        if char_stats[1] == 2:
            char_stats[6] += 12
            game_data.execute('select * from spells')
            for row in game_data:
                if row[4] == char_stats[3]:
                    spells.append([row[0], row[1], row[2], row[3], row[4]])
                    color(yellow)
                    print 'You have learned a new spell!'
    char_stats[5] = char_stats[6]

def stats():
    """Displays the characters current stats"""
    if char_stats[1] == 1 or char_stats[1] == '1':
        char_class = 'Fighter'
    if char_stats[1] == 2 or char_stats[1] == '2':
        char_class = 'Sorcerer'
    color(yellow)
    print '''
Name        : %s
Class       : %s
AC          : %s
Level       : %s       Experience: %s
Health      : %s/%s                               
Strength    : %s      Dexterity : %s
Constitution: %s      Wisdom    : %s
'''%(char_stats[0], char_class, char_stats[2]+ac_bonus, char_stats[3], char_stats[4],
     char_stats[5], char_stats[6], char_stats[7], char_stats[8], char_stats[9],
     char_stats[10])
    if len(weapons) < 1:
        m = 1
        mx = 4
    else:
        m = 0
        mx = 0
    m = m + weapon_stats[2] + round((char_stats[7] - 10)/2) + round(char_stats[3]/2)
    mx = mx + weapon_stats[3] + round((char_stats[7] - 10)/2) +round(char_stats[3]/2)
    print 'Weapon Damage: %s - %s' % (m, mx)
    if char_stats[1] == 1:
        print 'Attack bonus : %s' % attack_bonus
    else:
        print 'Attack bonus : %s    Spell bonus: %s' % (round((char_stats[7] - 10)/2)\
                                                       + round(char_stats[3]/2), \
                                                       attack_bonus)
        
def write_data(cs='char_stats'):
    """Writes the user data into the file data file when any changes"""
    with open('./data/userdata.txt') as infile:
        with open('./data/userout.txt', u'w') as outfile:
            for s in infile:
                if s.strip():
                    s = list(s.strip().split())
                    if cs[0] == s[0]:
                        s = cs
                    outfile.write('%s %s %s %s %s %s %s %s %s %s %s\
                            %s %s %s %s\n'\
                                  %(s[0], s[1], s[2], s[3], s[4], s[5], 
                                      s[6], s[7], s[8], s[9], s[10], 
                                      s[11], s[12], s[13], s[14]))
    os.rename('./data/userdata.txt', u'./data/userdata.tmp')
    os.rename('./data/userout.txt', u'./data/userdata.txt')
    os.remove('./data/userdata.tmp')
    
def combat(level=0):
    """ Calls the combat function

    Arguments:
    level - lvl for the enemy

    Returns:
    True or False for if you survived.

    """
    global attack_points
    s = []
    escape = False
    level = char_stats[3] + level
    game_data.execute('''select name, level, AC, bonus, mindmg, maxdmg, hp,\
init, fort, will, attack from monsters where level=%s''' % char_stats[3])
    for row in game_data:
        s.append(row)
    n = random.randint(0, len(s)-1)
    t = s[n]
    monster = list(t)
    color(yellow)
    print 'You have encountered a', monster[0]
    # special attack sequence
    def special_attack(ui):
        global attack_points
        ui = ui[0]
        ui = int(ui)
        attack_points -= 1
        attack = random.randint(1,20) + attack_bonus
        if char_stats[1] == 2:
            dmg = random.randint(spells[ui-1][2],\
                                 spells[ui-1][3]) + attack_bonus
            if attack >= monster[9] + 10:
                color(red)
                print 'You hit %s with your %s for %s damage!'\
                      % (monster[0], spells[ui-1][1],dmg)
            else:
                dmg = round(dmg/2)
                color(red)
                print 'Your %s grazed %s for %s damage!' \
                      % (spells[ui-1][1], monster[0], dmg)
        else:
            attack += weapon_stats[4]
            dmg = random.randint(weapon_stats[2], weapon_stats[3]) + \
                  round((char_stats[7] - 10)/2) + round(char_stats[3]/2)
            dmg = dmg * spells[ui-1][3]
            if attack >= monster[8] + 10:
                color(red)
                print 'You hit %s with your %s for %s damage!'\
                      % (monster[0], spells[ui-1][1],dmg)
            else:
                dmg = 0
                color(yellow)
                print 'Your %s missed %s!' \
                      % (spells[ui-1][1], monster[0])
        monster[6] -= dmg

    # Character attack sequence. 
    def char_attack():
        att = False
        while att != True:
            if len(spells) == 0 or attack_points == 0:
                color(blue)
                print '(A)ttack or (R)un?'
                user_input = prompt(['A', u'R'],u'[%s:%s]>' % \
                                    (char_stats[5], attack_points))
            else:
                sp = []
                color(blue)
                for row in spells:
                    sp.append(unicode(row[0]))
                print '(A)ttack, (S)pecials [1-%s] (R)un?' % len(spells)
                user_input = prompt(sp + ['A', u'S', u'R'], u'[%s:%s]>'\
                                    % (char_stats[5], attack_points))
            user_input = user_input[0]
            if user_input == 'A':
                if len(weapons) == 0:
                    attack = random.randint(1,20) + round((char_stats[7] - 10)/2) \
                             + round(char_stats[3]/2)
                    dmg = random.randint(1,4) + round((char_stats[7] - 10)/2) \
                              + round(char_stats[3]/2)
                    if attack >= monster[2]:
                        color(red)
                        print 'You punch %s for %s damage!' % (monster[0], dmg)
                    elif attack >= monster[2] - 5:
                        color(red)
                        dmg = round(dmg/2)
                        if dmg < 1: dmg = 1
                        print 'You slap %s for %s damage!' % (monster[0], dmg)
                    else:
                        color(yellow)
                        dmg = 0
                        print 'You punch at %s but miss!' % monster[0]
                else:
                    if char_stats[1] == 1:
                        attack = random.randint(1,20) + attack_bonus
                    else:
                        attack = random.randint(1,20) + round((char_stats[7] - 10)/2)\
                                 + round(char_stats[3]/2)
                    dmg = random.randint(weapon_stats[2], weapon_stats[3]) + \
                          round((char_stats[7] - 10)/2) + round(char_stats[3]/2)
                    if char_stats[1] == 1:
                        dmg += weapon_stats[4]
                    color(red)
                    if attack >= monster[2]:
                        print 'You hit %s with your %s for %s damage!' \
                              % (monster[0], weapons[0][0], dmg)
                    elif attack >= monster[2] - 5:
                        dmg = round(dmg/2)
                        if dmg < 1: dmg = 1
                        print 'You graze %s with your %s for %s damage!' \
                              % (monster[0], weapons[0][0], dmg)
                    else:
                        color(yellow)
                        dmg = 0
                        print 'You miss %s!' % monster[0]
                monster[6] -= dmg
                att = True
            elif user_input == 'S':
                color(yellow)
                print "Special ability's:"
                color(red)
                for row in spells:
                    print '%s - %s' % (row[0], row[1])
                    att = False
            elif user_input in sp:
                special_attack(user_input)
                att = True
            elif user_input == 'R':
                color(yellow)
                print 'You try to flee...'
                escape = random.randint(1,100)
                att = True
                if escape >= 25:
                    return True
    
    def mon_attack():
        " Monster attack sequence. "
        attack = random.randint(1,20) + monster[3]
        if attack > char_stats[2]:
            dmg = random.randint(monster[4], monster[5])
            color(red)
            print '%s %s you for %s damage!' % (monster[0], monster[10],\
                                                dmg)
            char_stats[5] -= dmg
        else:
            color(yellow)
            print '%s attacks and misses!' % monster[0]
            
    init = random.randint(1,20) + init_bonus
    m_init = random.randint(1,20) + monster[7]
    if init >= m_init:
        while char_stats[5] > 0:
            escape = char_attack()
            if monster[6] <= 0: break
            mon_attack()
            if char_stats[5] <= 0: break
            if escape == True: break
    elif init < m_init:
        while char_stats[5] > 0:
            mon_attack()
            if char_stats[5] <= 0: break
            escape = char_attack()
            if monster[6] <= 0: break
            if escape == True: break
    if char_stats[5] <= 0:
        return False
    elif escape == True:
        color(yellow)
        print 'You narrowly escape the', monster[0]
        return True
    elif monster[6] <= 0:
        gold = random.randint(1,4) * char_stats[3] 
        xp = (monster[1] + 1) * 3
        color(cyan)
        print 'You have slain %s, you get %sxp and find %s gold' % (monster[0],\
                                                                    xp,gold)
        char_stats[4] += xp
        if char_stats[4] >= (char_stats[3]*10)**2:
            print 'You have enough experience points to reach level %s!' \
                  % (char_stats[3] + 1)
        char_stats[11] += gold
        return True
    
def room(x, y):
    """ Calls the function to display room descriptions based on locations."""
    if x == 6:
        if y == 5:
            call_menu('townsquare.txt')
        elif y == 2:
            call_menu('mainstreet.txt')
            color(yellow)
            print "There is a sign for a Dwarven Armor Shop to the west."
        elif y == 8:
            call_menu('mainstreet.txt')
            color(yellow)
            print "There is a sign for Wolfgar's Weapon Shop to the west."
        else:
            call_menu('mainstreet.txt')
    elif x == 5:
        if y == 2:
            call_menu('armorshop.txt')
        elif y == 8:
            call_menu('weaponshop.txt')
        elif y == 5:
            call_menu('centerstreet.txt')
    elif y == 5 and x > 3 and x < 9:
        if x == 7:
            call_menu('centerstreet.txt')
        elif x == 4:
            call_menu('forestent.txt')
        elif x == 8:
            call_menu('catacombsent.txt')
    elif x <= 3:
        call_menu('forest.txt')
        if x == 3:
            if y == 5:
                color(yellow)
                print 'Forest entrance is to the east of here.'
    elif x >= 9:
        call_menu('catacombs.txt')
        if x == 9:
            if y == 5:
                color(yellow)
                print 'Catacombs entrance is to the west of here.'
        
# function to import data from the users database
def db_read():
    """ Reads data from the users database file """
    global inventory
    global weapons
    global armor
    global spells
    conn2 = sqlite3.connect('./data/%s.dat' % char_stats[0])
    user_data = conn2.cursor()
    user_data.execute('select name, tbl, number from inventory')
    t = user_data.fetchall()
    inventory = list(list(x) for x in t)
    user_data.execute('select name, tbl, number from weapons')
    t = user_data.fetchall()
    weapons = list(list(x) for x in t)
    user_data.execute('select name, tbl, number from armor')
    t = user_data.fetchall()
    armor = list(list(x) for x in t)
    user_data.execute('select * from spells')
    t = user_data.fetchall()
    spells = list(list(x) for x in t)
    conn2.close()
    
def db_write():
    """ Saves user database. """
    conn2 = sqlite3.connect('./data/%s.dat' % char_stats[0])
    user_data = conn2.cursor()
    user_data.execute('delete from inventory')
    user_data.executemany('''insert into inventory (name, tbl, number) \
values (?, ?, ?)''', inventory)
    user_data.execute('delete from weapons')
    user_data.executemany('''insert into weapons (name, tbl, number) \
values (?, ?, ?)''', weapons)
    user_data.execute('delete from armor')
    user_data.executemany('''insert into armor (name, tbl, number) \
values (?, ?, ?)''', armor)
    user_data.execute('delete from spells')
    user_data.executemany('''insert into spells (id, name, mindmg, maxdmg, \
level) values (?, ?, ?, ?, ?)''', spells)
    conn2.commit()
    conn2.close()

def refresh_data():
    """ Refreshes the weapon and armor_stats variables and all other
    user data and stats
    """
    global weapon_stats
    global armor_stats
    global ac_bonus
    ac_bonus = 0
    global attack_bonus
    attack_bonus = 0
    global init_bonus
    init_bonus = 0
    if len(weapons) >= 1:
        game_data.execute('select * from weapons where id=%s' % weapons[0][2])
        weapon_stats = game_data.fetchone()
        #print(weapon_stats)
    else:
        weapon_stats = (0,'',0,0,0,0,0)
    if len(armor) >= 1:
        game_data.execute('select * from armor where id=%s' % armor[0][2])
        armor_stats = game_data.fetchone()
        #print(armor_stats)
    else:
        armor_stats = (0,'',0,0,0,0)
    if char_stats[1] == 1:
        if armor_stats[5] != 1:
            ac_bonus = round((char_stats[8] - 10)/2)
        ac_bonus = ac_bonus + armor_stats[2] + armor_stats[3]\
                   + round(char_stats[3]/2)
        attack_bonus = round((char_stats[7] - 10)/2) + round(char_stats[3]/2)\
                       + weapon_stats[4]
        init_bonus = round((char_stats[8] - 10)/2) + round(char_stats[3]/2)
    if char_stats[1] == 2:
        if armor_stats[5] != 1:
            if char_stats[10] > char_stats[8]:
                ac_bonus = round((char_stats[10] - 10)/2) + armor_stats[2] \
                           + armor_stats[3] + round(char_stats[3]/2)
            else:
                ac_bonus = round((char_stats[8] - 10)/2) + armor_stats[2] \
                           + armor_stats[3] + round(char_stats[3]/2)
            attack_bonus = round((char_stats[10] - 10)/2) + \
                           round(char_stats[3]/2)
        else:
            ac_bonus = armor_stats[2] + armor_stats[3] + round(char_stats[3]/2)
            attack_bonus = (round((char_stats[10] - 10)/2) + \
                           round(char_stats[3]/2))
        init_bonus = (round((char_stats[8] - 10)/2) + round(char_stats[3]/2)) \
                     + 2

def item_list(tbl):
    """ Lists either weapons or armor available from a vendor. """
    color(yellow)
    if tbl == 'weapons':
        game_data.execute('select * from weapons')
        for row in game_data:
            print row[1], '.' * (28 - len(row[1])), u'%sgp' % row[5]
    elif tbl == 'armor':
        game_data.execute('select * from armor')
        for row in game_data:
            print row[1], '.' * (28 - len(row[1])), u'%sgp' % row[4]

def buy(tbl, item):
    """ Buys an item from a shop """
    item = item.title()
    if tbl == 'weapons':
        game_data.execute('select * from weapons')
        for row in game_data:
            if row[1] == item:
                if row[5] > char_stats[11]:
                    color(yellow)
                    print "You don't have enought gold for", row[1]
                    break
                else:
                    inventory.append([row[1], 'weapons', row[0]])
                    char_stats[11] = char_stats[11] - row[5]
                    color(yellow)
                    print 'You bought', item
                    break
        if row[1] != item:
            print 'Item does not exist'
    if tbl == 'armor':
        game_data.execute('select * from armor')
        for row in game_data:
            if row[1] == item:
                if row[4] > char_stats[11]:
                    color(yellow)
                    print "You don't have enough gold for", row[1]
                    break
                else:
                    inventory.append([row[1], 'armor', row[0]])
                    char_stats[11] = char_stats[11] - row[4]
                    color(yellow)
                    print 'You bought', item
                    break
        if row[1] != item:
            print 'Item does not exist'

def sell(item):
    """ Sells items from your inventory to a shop keeper """
    color(yellow)
    item = item.title()
    count = -1
    for row in inventory:
        count += 1
        if row[0] == item:
            inventory.remove(inventory[count])
            game_data.execute('select * from %s where id=%s' % (row[1], row[2]))
            sell_item = game_data.fetchone()
            if row[1] == 'armor':
                sell_price = round(sell_item[4]/5)
            else:
                sell_price = round(sell_item[5]/5)
            char_stats[11] += sell_price
            print 'You sold %s for %s gold' % (row[0], sell_price)
            break
    if row[0] != item:
        print 'You do not have %s.' % item                  
        
# this gets your character info from the user file, or creates a new one for you
try:
    os.system('clear')
except:
    pass
login = ""
color(green)
print 'Welcome to PySUD, the Python Single User Dungeon!'
while login == "":
    login = (raw_input('\nPlease enter your character name: '))
login = login.capitalize()
#open the user data file
data_file = open('./data/userdata.txt', u'r')
# for/else loop to search the user file for your character
for line in data_file:
    if line.strip():
        char_stats = list(line.strip().split())
        # if it is found, breaks the loop
        if login == char_stats[0]:
            data_file.close()
            pw = ""
            while pw != char_stats[12]:
                sys.stdout.write('Please enter your password: ')
                os.system('stty -echo')
                pw = raw_input()
                print ''
                os.system('stty echo')
            break
# if the whole file has been read and no id was found, we create a new one
else:
    data_file.close()
    print 'Character name not found, lets create a new character!'
    pause()
    call_menu('class.txt')
    aok = False
    # choose the character class
    while aok == False:
        char_class = (raw_input('What class would u like to be? [1/2]:'))
        if char_class == '1':
            aok = ask_ok('You chose to be a FIGHTER, is that correct? [y/n]:')
            char_stats = [login, 1, 10, 1, 0, 15, 15, 10, 8, 10, 8, 0, '', 6, 0]
        if char_class == '2':
            aok = ask_ok('You chose to be a SORCERER, is that correct? [y/n]:')
            char_stats = [login, 2, 10, 1, 0, 9, 9, 8, 10, 8, 10, 0, '', 6, 0]
          
    # lets you select a new new character name
    # this module is ommited for the time being, as its not really needed
    # and im failing at coding it properly!
    #aok = False   
    #while aok == False:
    #    print('Your characters name will be', login,)
    #    aok = ask_ok("is that ok? [y/n]:")
    #    if aok == True:
    #        break
    #    if aok == False:
    #        data_file = open('./data/userdata.txt', 'r')
    #        while aok == False:
    #            login = (input('Please enter a new name for your character: '))
    #            login = login.capitalize()
    #            for line in data_file:
    #                if line.strip():
    #                    char_stats = list(line.strip().split())
    #                    print(char_stats)
    #                # if it is found, breaks the loop
    #            if login == char_stats[0]:
    #                print('That name is already taken!')
    #                aok == False
    #                break
                
    #            print('Your character will be named:', login)
    #            aok = ask_ok('Are you sure this is the name you want? [y/n]:')                

    # Now its time to select your character stats
    call_menu('stats.txt')
    
    # call the function to assign stat points
    level_up(16)
    print '\nNow you must select a password to keep others from playing your character,'
    password = "a"
    pw_verify = ""
    while len(password) < 5 and password != pw_verify:
        password = (raw_input('Please enter a password (5 characters or more):'))
        while len(password) >= 5 and password != pw_verify:
            pw_verify = (raw_input('Please re-enter your password:'))
    char_stats[12] = password
    with open('./data/userdata.txt', u'a') as data_file:
        data_file.write('%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s'\
                        %(char_stats[0], char_stats[1], char_stats[2],
                          char_stats[3], char_stats[4], char_stats[5],
                          char_stats[6], char_stats[7], char_stats[8],
                          char_stats[9], char_stats[10], char_stats[11],
                          char_stats[12], char_stats[13], char_stats[14]))
        data_file.close()
    try:
        conn2 = sqlite3.connect('./data/%s.dat' % char_stats[0])
        user_data = conn2.cursor()
        user_data.execute('''create table inventory (name text, tbl text, \
number int)''')
        user_data.execute('''create table weapons (id integer primary key, \
name text, tbl text, number int)''')
        user_data.execute('''create table armor (id integer primary key, \
name text, tbl text, number int)''')
        user_data.execute('''create table spells (id integer primary key, \
name text, mindmg int, maxdmg int, level int)''')
        conn2.close()
    except:
        pass
    db_read()
    # gets 1st level spells for Sorcerer
    if char_stats[1] == 2 or char_stats[1] == '2':
        game_data.execute('select * from spells')
        for row in game_data:
            if row[4] == char_stats[3]:
                spells.append([row[0], row[1], row[2], row[3], row[4]])
                db_write()

        
#convert stats into integers before starting game loop
char_stats[1] = int(char_stats[1])
char_stats[2] = int(char_stats[2])
char_stats[3] = int(char_stats[3])
char_stats[4] = int(char_stats[4])
char_stats[5] = int(char_stats[5])
char_stats[6] = int(char_stats[6])
char_stats[7] = int(char_stats[7])
char_stats[8] = int(char_stats[8])
char_stats[9] = int(char_stats[9])
char_stats[10] = int(char_stats[10])
char_stats[11] = int(char_stats[11])
char_stats[13] = int(char_stats[13])
char_stats[14] = int(char_stats[14])

# Reads the players database
db_read()

#main gaming loop!
x, y = char_stats[13], char_stats[14]
user_input = [""]
living = True
moves = 0
# remove for main game, here for debugging only
#print(inventory)
#print(weapons)
#print(armor)
#print(spells)
# end of remove
# sets the number of attack points per level

if char_stats[1] == 1:
    attack_points = round(char_stats[3]/2)
else:
    attack_points = (round(char_stats[3]/2)) + 1
ap_max = attack_points
refresh_data()
call_menu('motd.txt')
pause()
leader_board()
os.system('clear')
room(x,y)
while user_input[0] != 'CAMP':
    if living == False:
        color(white)
        print '''
You have been killed.  Would you like to make an offering to the gods in hopes
of ressurection?'''
        res = ask_ok('yes/no: ')
        char_stats[5] = 1
        if res == False: break
        elif res == True:
            char_stats[11] -= 1
            color(yellow)
            print '''
Your feel cold and disoriented, like you have just woken up from a bad dream.
You are badly wounded but alive, you had better rest.'''
            living = True
    moves += 1
    if moves == 4:
        char_stats[13] = x
        char_stats[14] = y
        write_data(char_stats)
        db_write()
        moves = 0
    #refresh_data()
    directions = ''
    if y+1 <= len(dungeon[x])-1 and dungeon[x][y+1] == 0:
        directions = 'N'
    if y-1 >= 0 and dungeon[x][y-1] == 0:
        directions = directions + 'S'
    if x+1 <= len(dungeon)-1 and dungeon[x+1][y] == 0:
        directions = directions + 'E'
    if x-1 >= 0 and dungeon[x-1][y] == 0:
        directions = directions + 'W'

    # Converts the string of valid directions into a list.
    valid_inputs = [directions[i:i+1] for i in xrange(0,len(directions),1)]
    #room(x,y)
    color(blue)
    print '\nPossible exits are:', valid_inputs
    user_input = prompt(valid_inputs + ['CAMP', u'STATS', u'LOOK', u'HELP',
                                        'LEVEL', u'REST', u'INVENTORY', u'EQUIP',
                                        'LIST', u'BUY', u'SELL', u'LOCATION',
                                        'RANK', u'MAP'],
                        '[%s:%s]>' % (char_stats[5], attack_points), \
                        'Invalid command, type "HELP" for command list.')
    if user_input[0] == 'RANK':
        leader_board()
    if user_input[0] == 'MAP':
        call_menu('map.txt')
    if user_input[0] == 'LIST':
        if x == 5 and y == 2:
            item_list('armor')
        elif x == 5 and y == 8:
            item_list('weapons')
        else:
            color(yellow)
            print 'You are not in a shop.'
    if user_input[0] == 'SELL':
        if len(user_input) != 2:
            color(yellow)
            print 'You did not say what item you wanted to sell!'
        else:
            if x == 5 and y == 2 or x == 5 and y == 8:
                sell(user_input[1])
            else:
                color(yellow)
                print 'There is nobody here to buy your %s.' % user_input[1]
    if user_input[0] == 'BUY':
        if len(user_input) != 2:
            color(yellow)
            print 'You did not say what item you wanted to buy!'
        else:
            if x == 5 and y == 2:
                buy('armor', user_input[1])
                char_stats[13] = x
                char_stats[14] = y
                write_data(char_stats)
                db_write()
            elif x == 5 and y == 8:
                buy('weapons', user_input[1])
                char_stats[13] = x
                char_stats[14] = y
                write_data(char_stats)
                db_write()
            else:
                color(yellow)
                print 'There is nobody here to buy %s from.' % user_input[1]
    if user_input[0] == 'STATS':
        stats()
    if user_input[0] == 'INVENTORY':
        color(yellow)
        if len(inventory) == 0:
            sys.stdout.write('You dont have anything in your inventory.')
        else:
            sys.stdout.write('You are carrying ')
            for row in inventory:
                sys.stdout.write('%s, ' % row[0])
        if len(weapons) == 0:
            print '\nYou have nothing in your hands.'
        elif len(weapons) == 1:
            print '\nYou have a %s in your hand.' % weapons[0][0]
        elif len(weapons) == 2:
            print '\nYou are holding %s, %s in your hands.' \
                  % (weapons[0][0], weapons[1][0])
        if len(armor) == 0:
            print 'You are wearing nothing of interest.'
        elif len(armor) > 0:
            print 'You are wearing %s.' % armor[0][0]
        print 'You have %s gold coins in your pouch.' % char_stats[11]
        color(white)
    if user_input[0] == 'EQUIP':
        if len(user_input) != 2:
            color(yellow)
            print 'You did not say what you wanted to equip!'
        else:
            eq_item = user_input[1]
            color(yellow)
            eq_item = eq_item.title()
            count = -1
            for row in inventory:
                count += 1
                if row[0] == eq_item:
                    if row[1] == 'weapons':
                        if len(weapons) > 0:
                            inventory.append(weapons[0])
                        weapons = [[eq_item, 'weapons', row[2]]]
                    elif row[1] == 'armor':
                        if len(armor) > 0:
                            inventory.append(armor[0])
                        armor = [[eq_item, 'armor', row[2]]]
                    print 'You have equiped', eq_item
                    inventory.remove(inventory[count])
                    char_stats[13] = x
                    char_stats[14] = y
                    write_data(char_stats)
                    db_write()
                    refresh_data()
                    break
            else:
                print "You don't have %s in your inventory!" % eq_item
        
    if user_input[0] == 'N':
        y += 1
        if x <= 3 or x >= 9:
            living = combatroll()
        if living != False: room(x,y)
    if user_input[0] == 'S':
        y -= 1
        if x <= 3 or x >= 9:
            living = combatroll()
        if living != False: room(x,y)
    if user_input[0] == 'E':
        x += 1
        if x <= 3 or x >= 9:
            living = combatroll()
        if living != False: room(x,y)
    if user_input[0] == 'W':
        x -= 1
        if x <= 3 or x >= 9:
            living = combatroll()
        if living != False: room(x,y)
    if user_input[0] == 'HELP':
        call_menu('help.txt')
    if user_input[0] == 'LOOK':
        room(x,y)
    if user_input[0] == 'LEVEL':
        if char_stats[4] >= (char_stats[3]*10)**2:
            color(yellow)
            print 'You have gained a new level!'
            char_stats[3] = char_stats[3] + 1
            if char_stats[1] == 1:
                attack_points = round(char_stats[3]/2)
            else:
                attack_points = (round(char_stats[3]/2)) + 1
            ap_max = attack_points
            level_up(1)
            char_stats[13] = x
            char_stats[14] = y
            write_data(char_stats)
            db_write()
            refresh_data()
            moves = 0
        else:
            color(yellow)
            print '\nYou need', (char_stats[3]*10)**2 - char_stats[4],\
                  'more experience points to reach level %s!\n' %\
                  (char_stats[3] + 1)
    if user_input[0] == 'REST':
        color(yellow)
        print 'Resting...'
        if char_stats[5] == char_stats[6]:
            while attack_points < ap_max:
                attack_points += 1
                time.sleep(1)
        else:
            while char_stats[5] != char_stats[6]:
                char_stats[5] += 2 * char_stats[3]
                if char_stats[5] > char_stats[6]:
                    char_stats[5] = char_stats[6]
                if attack_points < ap_max:
                    attack_points = ap_max
                time.sleep(1)
                #if x <= 3 or x >= 9:
                 #   monster = random.randint(1,100)
                  #  if monster < 10:
                   #     living = combat()
                    #    break
    if user_input[0] == 'LOCATION':
        color(cyan)
        print 'Location co-ordinates X=%s Y=%s' % (x,y)

print 'Thanks for playing!'    
char_stats[13] = x
char_stats[14] = y
write_data(char_stats)
db_write()
    
conn.close()


