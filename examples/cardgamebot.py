# COMP10001 Foundations in Computing Project 2 Question 5
# ABRREVIATIONS:
# -- 'acc' means 'accumulation'
# -- 'val' means 'value'
# -- 'freq' means 'frequency'

from collections import defaultdict as dd
from itertools import combinations

VAL, SUIT, MIN_NATURAL, MAX_WILDS, MAX_RUN_LEN = 0, 1, 2, 8, 12
RUN_ORDER = ['2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K', '2', 
             '', '']
COLOUR = {'D': 'red', 'H': 'red', 'C': 'black', 'S': 'black'}
WILDS = ['AC', 'AD', 'AH', 'AS']
ACC_VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 
              '0': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 1}
SCORE_VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                '0': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 25}
PLAY_ORDER = {1: [5, None], 2: [5, None], 3: [1, 2], 4: [1, 2, 3, 4], 
              5: [1, 2, 3, 4]}  # {play_type: [valid prev_play_types], ...}
ACC_TOTALS = [34, 55, 68, 76, 81, 84, 86, 87, 88]
PHASE_GROUPS = {1: [[1], [1]], 2: [[2]], 3: [[6], [6]], 4: [[3], [3]], 
                5: [[4]], 6: [[6, 7], [6, 7]], 7: [[5], [3]]}

# HELPER FUNCTIONS TO FIND GROUPS
##############################################################################
def colour_check(group, aces_check=False):
    '''
    Check if `group` is a set of cards of the same colour.
    Arguments:
        group(list): list of cards
        aces_check(bool, opt): checks if aces are the same colour too
        -- for phase 6: accumulation of cards of same colour
    Returns:
        bool: True if group is a set of cards of the same colour and False 
            otherwise.
    '''
    num_cards = len(group)
    colour_dict = dd(int)
    
    # store frequency counts of colours in `colour_dict`
    for card in group:
        if card in WILDS and not aces_check:
            colour_dict['wilds'] += 1
        else:
            colour_dict[COLOUR[card[SUIT]]] += 1
            
    # check if the natural and wild cards make up the correct total
    if colour_dict['red'] + colour_dict['wilds'] == num_cards \
        or colour_dict['black'] + colour_dict['wilds'] == num_cards:
        return True
    
    # incorrect total - invalid set
    return False

def run_check(group, max_wild, ref='', wild_count=0):
    '''
    Check if `group` is a valid run of cards. [Recursive]
    Arguments:
        group(list): list of cards
        max_wild(int): maximum number of wild cards allowed in the run
    Local variables:
        ref(str): reference value for next card
        wild_count(int): number of wild cards in run
    Returns:
        bool: True if group is a run of card; False otherwise
    '''
    # BASE: maximum wild count exceeded
    if wild_count > max_wild:
        return False

    # BASE: finished checking whole group
    elif not group:
        return True

    # wild card - add to the wild count increment reference value
    elif group[0] in WILDS:
        return run_check(group[1:], max_wild,
            RUN_ORDER[RUN_ORDER.index(ref) + 1], wild_count + 1)

    # first card/follows sequence - update reference value for the next card
    elif group[0][VAL] == ref or ref == '':
        return run_check(group[1:], max_wild,
            RUN_ORDER[RUN_ORDER.index(group[0][VAL]) + 1], wild_count)

    # BASE: card no longer follows the run sequence
    return False

def acc_valid(val_list, acc_total=0, acc_list=ACC_TOTALS):
    '''
    Return True if accumulation is complete; False if it surpassed the next 
    accumulation goal (invalid); None if it is not complete yet. [Recursive]
    Arguments:
        val_list(list): list of card's values ['2', 'A', ...]
    Local Variables:
        acc_total(int): current accumulation total
        acc_list(list): 
    Returns:
        bool: 
            -- True if accumulation is complete
            -- False if next accumulation goal surpassed (invalid)
            -- None if accumulation is not complete yet
    '''
    # BASE: acc goal surpassed or maximum acc surpassed - invalid
    if not acc_list or acc_total > acc_list[0]:
        return False
    
    # BASE: group completed and goal total reached - complete
    elif not val_list and acc_total == acc_list[0]:
        return True
    
    # BASE: group completed but goal not yet reached - incomplete
    elif not val_list and acc_total < acc_list[0]:
        return None
    
    # acc goal reached - move on to next goal
    elif acc_total == acc_list[0]:
        return acc_valid(val_list[1:], acc_total + val_list[0], acc_list[1:])
    
    # acc goal not yet reached - continue working towards current goal
    elif acc_total < acc_list[0]:
        return acc_valid(val_list[1:], acc_total + val_list[0], acc_list)


# HELPER FUNCTIONS TO FIND PHASES
# -- used in Play Types 1 and 5 to rank cards, and Play Type 3 to find phases
##############################################################################
def find_set_phase(hand, phase_type, ranking=True):
    '''
    Finds phases that require sets of cards of same values or suits.
    Arguments:
        hand(list): list of cards in hand
        phase_type(int): player's current phase
        ranking(opt. bool): True if function is used for ranking cards (Play
                            Types 1 and 5); False otherwise.
    Returns:
        remainder(list): remainder(list): list of remaining cards in hand after 
            complete/partially complete phases/groups are removed
        phase_list:
            -- ranking=True: (list) list of complete groups (ie. (a), (b))
            -- ranking=False: (2d list) list of complete/partial groups (ie. 
                                (a), (b), (c), (d))
        phase_complete(bool):
            -- True: complete phase found
            -- None: partial phase found
            -- False: no phase found
    '''
    def find_partial_sets(freq_dict):
        '''
        Finds 'partial set cards', which are cards with high value/suit 
        frequencies (but not high enough to be a valid set) and separates 
        them from '(non-partial) remainders', which are the cards of the lowest
        frequency.
        Arguments:
            freq_dict(dd): either a val dict or suit dict, depending on phase
                -- phases 1, 4, 7: {val1: [cards of val1], ...} 
                -- phase 2: {suit1: [cards of suit1], ...} 
        Returns:
            partials(list): list of 'partial set cards'
            remainder(list): list of remaining cards in hand after 
                partials are removed
        '''
        # find the lowest frequency in `freq_dict`
        lengths_list = [len(card_list) for card_list in 
            list(freq_dict.values())]
        lowest_freq = min(lengths_list)

        remainder = []
        partials = []
        scores_dict = dd(int)

        # (i) Rank keys by frequency
        for key, card_list in list(freq_dict.items()):

            # add keys of lowest frequency to `remainder`
            if len(card_list) == lowest_freq:
                freq_dict.pop(key)
                remainder += card_list
            
            # partials' keys - calculate total score value for tie breaking
            else:
                total_score_val = 0
                for card in card_list:
                    total_score_val += SCORE_VALUES[card[VAL]]
                scores_dict[key] = total_score_val

        # (ii) Tie break by total score value
        # sort from lowest_freq to largest score val
        partial_item_list = sorted(list(freq_dict.items()), key=lambda item: 
                                    (-len(item[1]), scores_dict[item[0]]))

        # unpack `partial_item_list`(dd item list) --> `partials`(list)
        for key, card_group in partial_item_list:
            # (3) Rank individual cards by 
            card_group.sort(key=lambda c: SCORE_VALUES[c[VAL]])
            for card in card_group:
                partials.append(card)

        return partials, remainder
    
    phase_dict = {1: [3, 2, VAL], 2: [7, 1, SUIT], 4: [4, 2, VAL], 
                  7: [4, 1, VAL]}
    group_len = phase_dict[phase_type][0]
    phase_len = phase_dict[phase_type][1]
    mode  = phase_dict[phase_type][2]

    # sort from largest to smallest accumulation value
    hand.sort(key=lambda c: -ACC_VALUES[c[VAL]])

    freq_dict = dd(list)

    # store frequency counts of values/suits in `freq_dict`
    for card in hand:
        if card in WILDS:
            freq_dict['wild'].append(card)
        else:
            key = ACC_VALUES[card[VAL]] if mode == VAL else card[SUIT]
            freq_dict[key].append(card)
    
    phase_list = []
    remainder = []

    # (a) Complete Groups without Wilds
    for key, card_list in list(freq_dict.items())[:]:
        # phase complete - stop finding phases
        if len(phase_list) == phase_len:
            break
        # findng complete groups without wilds
        # -- check if frequency of card makes up group length
        elif key!='wild' and len(card_list) >= group_len:
            phase_list.append(card_list[:group_len])
            freq_dict[key] = card_list[group_len:]

    # (b) Complete Groups with Wilds
    for key, card_list in list(freq_dict.items())[:]:

        # phase complete - stop finding phases
        if len(phase_list) == phase_len:
            break

        # finding complete groups with wilds
        # -- check if the sum of natural and wild cards make up group length
        elif key != 'wild' and len(card_list) >= MIN_NATURAL \
            and len(card_list) + len(freq_dict['wild']) >= group_len \
                and len(phase_list) < phase_len:
            
            # group found - add to phase list
            new_card_list = card_list + freq_dict['wild'][:group_len
                - len(card_list)]
            phase_list.append(new_card_list)

            # update wild frequency
            freq_dict['wild'] = freq_dict['wild'][group_len - len(card_list):]
            freq_dict.pop(key)

    # check if phase is complete, partially complete or incomplete
    # -- update phase_complete flag and remainder list
    if len(phase_list) == phase_len:
        phase_complete = True
    elif 0 < len(phase_list) < phase_len:
        phase_complete = None
    else:
        phase_complete = False

    # update remainder when not ranking
    if not ranking:
        if phase_complete:
            remainder = flatten(list(freq_dict.values()))
        else:
            remainder = hand

    else: 
        # flatten phase list to 1 dimentional list
        phase_list = flatten(phase_list)

        # (c) Wild Cards
        # go through cards in `freq_dict` (dict)
        for key, _ in list(freq_dict.items())[:]:

            # find remaining wild cards
            # -- add wild cards to the `phase_list`
            if key == 'wild' and freq_dict[key]:
                phase_list += freq_dict[key]
                
                # remove wilds from initial remainder
                freq_dict.pop('wild')

            # remove empty frequencies
            elif not freq_dict[key]:
                freq_dict.pop(key)

        # (d) Partially Complete Groups
        if freq_dict:
            partial_set_cards, remainder = find_partial_sets(freq_dict)

            # add partial set cards to `phase_list`
            phase_list += partial_set_cards

    return remainder, phase_list, phase_complete

def find_acc_phase(hand, phase_type, ranking=True):
    '''
    Finds accumulation phases.
    Arguments:
        hand(list): list of cards in hand
        phase_type(int): player's current phase
        ranking(opt. bool): True if function is used for ranking cards (Play
                            Types 1 and 5); False otherwise.
    Returns:
        remainder(list): list of remaining cards in hand after 
            complete/incomplete phases are removed
        phase_list:
            -- ranking=True: (list) list of complete groups (ie. (a), (b))
            -- ranking=False: (2d list) list of complete/partial groups (ie. 
                                (a), (b), (c), (d))
        phase_complete (bool): True if the phase is complete; False otherwise
    '''
    def find_acc_group(cards, mode):
        '''
        Return an accumulation group.
        Arguments:
            cards(list): list of cards to find accumulation group from.
            mode(str): 
                `short` mode: Find an accumulation group starting from shortest
                                to longest combination of cards.
                `long` mode: Find an accumulation group starting from longest 
                                to shortest combination of cards.
        Returns:
            group_found(bool): True if a valid accumulation group is found; 
                                False otherwise.
            acc_group(list): List of cards in valid accumulation group or list
                                of cards whose total is closest to 34
            group_remainder(list): List of remaining cards after `acc_group`
                                    cards are removed from `cards`.
        '''
        # shortest and longest combination lengths
        shortest = 3
        longest = min(8, len(cards))

        # setting the order of combination sizes for each mode
        if mode == 'short':
            combination_sizes = range(shortest, longest)
        else:
            combination_sizes = range(longest, shortest - 1, -1)
        
        # sort from smallest to largest accumulation value
        # -- gets rid of more cards
        cards.sort(key=lambda c: ACC_VALUES[c[VAL]])

        group_found = False
        acc_group = []
        group_remainder = []
        promising_diff = 0

        # create combination of cards in hand
        # -- from shortest/longest combination (depending on `mode`)
        for r in combination_sizes:
            try:
                for comb in combinations(cards, r):
                    # check if the combination is a valid group totalling 34
                    acc_values = [ACC_VALUES[card[VAL]] for card in comb]
                    difference = sum(acc_values) - ACC_TOTALS[0]
                    if not difference:

                        # group 7 also needs to be same colour
                        if group_type == 7:
                            if not colour_check(comb, True):
                                continue

                        # group found
                        # valid accumulation group found - add to `phase_list`
                        acc_group = list(comb)
                        
                        # set group_found flag
                        group_found = True

                        raise StopIteration

                    # check if combination is closest to 34
                    elif difference <= promising_diff:
                        acc_group = list(comb)

            # break out of both loops when group found
            except StopIteration:
                break

        # add remaining cards to `remainder`(list)
        group_remainder = []
        for card in cards:
            if card not in acc_group:
                group_remainder.append(card)

        return group_found, group_remainder, acc_group

    phase_dict = {3: 6, 6: 7}
    group_type = phase_dict[phase_type]

    phase_list = []
    modes_list = ['long', 'short']

    # start by trying to find 2 long groups (longest possible acc phase)
    # if unsuccessful, then try to find 1 short and 1 long group
    for mode in modes_list:
        group_2_found = False

        # (1) Find 1st group
        group_1_found, group_1_remainder, group_1 = find_acc_group(hand, mode)

        # (2*) Find 2nd group - *only if first group found
        if group_1_found:
            group_2_found, remainder, group_2 = \
                find_acc_group(group_1_remainder, 'long')

        # both groups found - Phase is Complete
        if group_2_found:
            # add both groups to phase list
            phase_list.append(group_1)
            phase_list.append(group_2)

            phase_complete = True

            # break out of phase-finding loop
            break

        # 1 group found - Partial Phase Found
        elif mode == 'short' and group_1_found:
            # add complete group to phase_list
            phase_list.append(group_1)

            # add partial group (ie. group of cards whose total is closest
            # to 34) to phase_list
            phase_list.append(group_2)

            phase_complete = None
        
        # no complete groups found
        elif mode == 'short':
            # add partial group (ie. group of cards whose total is closest
            # to 34) to phase_list
            phase_list.append(group_1)

            # set remainder and phase_complete flag
            remainder = group_1_remainder
            phase_complete = False
    
    # flatten 2 dimentional phase list to 1 dimentional phase list
    if ranking:
        phase_list = flatten(phase_list)

    return remainder, phase_list, phase_complete

def find_run_phase(hand, phase_type, ranking=True):
    '''
    ranking=True: Return longest run in card_set
    ranking=False: Return run phase.
    '''
    phase_dict = {5: [8, 6], 7: [4, 2]}
    group_len = phase_dict[phase_type][0]
    max_wilds = phase_dict[phase_type][1]

    # separate hand into cards_set, wilds and duplicates
    card_set = []
    wilds = []
    duplicates = []
    card_set_vals = []

    # search through all the cards in hand
    for card in hand:

        # find wilds
        if card in WILDS:
            wilds.append(card)

        # find unique cards
        elif card[VAL] not in card_set_vals:
            card_set.append(card)
            card_set_vals.append(card[VAL])

        # find duplicates
        else:
            duplicates.append(card)

    # hand is all aces
    if not card_set:
        return hand, [], False

    # sort from smallest to largest accumulation values
    card_set.sort(key=lambda c: ACC_VALUES[c[VAL]])
    card_set_vals.sort(key=lambda v: ACC_VALUES[v])

    longest_run = []

    # Generate runs starting from every possible starting value (from 2 to K)
    # and find for longest possible run
    # -- eg. ['<starting_val>, ...], ['2_',...], ['3_'...], ...
    # -- every <starting_val> can also be a wild
    for i in range(MAX_RUN_LEN):
        # create copies - reset to 'original values' when generating each run
        card_set_vals_copy = card_set_vals[:]
        card_set_copy = card_set[:]
        wilds_copy = wilds[:max_wilds]

        # create a reference value list (run values starting with starting_val)
        ref_val_list = [RUN_ORDER[k % 12] for k in range(i, MAX_RUN_LEN + i)]
        group = []
        for j in range(MAX_RUN_LEN):
            # card value not in hand - use wilds
            if ref_val_list[j] not in card_set_vals_copy:
                # no more wilds in hand
                if not wilds_copy:
                    break
                # add wild to group
                else:
                    group.append(wilds_copy.pop())

            # card value in hand - add card to group
            else:
                # index of card in card_set_vals
                index = card_set_vals_copy.index(ref_val_list[j])
                card_set_vals_copy.pop(index)
                group.append(card_set_copy.pop(index))
    
        # find for the longest run
        if len(group) >= len(longest_run):
            longest_run = group

    phase_list = longest_run[:]

    # Find remainders
    remainder = hand[:]
    for card in phase_list:
        remainder.remove(card)

    # Update phase_complete
    # run phase found
    if len(longest_run) >= group_len:
        phase_complete = True
        if not ranking:
            phase_list = [longest_run[:group_len]]

    # partial or no run found
    else:
        phase_complete = None if longest_run else False
        if not ranking:
            remainder = card_set + duplicates
            phase_list = []

    return remainder, phase_list, phase_complete

def find_phase_7(hand, phase_type, ranking=True):
    '''
    Finds phase 7 phases.
    Arguments:
        hand(list): list of cards in hand
        phase_type(int): player's current phase
        ranking(opt. bool): True if function is used for ranking cards (Play
                            Types 1 and 5); False otherwise.
    Returns:
        remainder(list): list of remaining cards in hand after 
            complete/incomplete phases are removed
        phase_list:
            -- ranking=True: (list) list of complete groups (ie. (a), (b))
            -- ranking=False: (2d list) list of complete/partial groups (ie. 
                                (a), (b), (c), (d))
        phase_complete (bool): True if the phase is complete; False otherwise
    '''
    remainder = []
    phase_list = [[], []]

    def find_run_group(cards):
        '''Finds group 5 (run group).'''

        red_run_group = []
        black_run_group = []
        red_run_remainder = []
        black_run_remainder = []
        run_found = False

        red_stack = []
        black_stack = []
        wild_stack = []

        # split group into red, black and wild stacks
        for card in cards:
            if card in WILDS:
                wild_stack.append(card)
            elif COLOUR[card[SUIT]] == 'red':
                red_stack.append(card)
            elif COLOUR[card[SUIT]] == 'black':
                black_stack.append(card)

        red_run_complete = None
        black_run_complete = None

        # check red stack for runs
        if bool(len(red_stack) + len(wild_stack)):
            red_run_remainder, red_run_group, red_run_complete = \
                find_run_phase(red_stack + wild_stack, phase_type)

        # check black stack for runs
        if bool(len(black_stack) + len(wild_stack)) and not red_run_complete:
            black_run_remainder, black_run_group, black_run_complete = \
                find_run_phase(black_stack + wild_stack, phase_type)

        # Run found
        # -- red run found
        run_group = []
        if red_run_complete: 
            run_remainder = red_run_group[4:] + red_run_remainder + black_stack
            run_group = red_run_group[:4]  # 4 cards in a group
            run_found = True
        
        # -- black run found
        elif black_run_complete:
            run_remainder = black_run_group[4:] + black_run_remainder \
                + red_stack
            run_group = black_run_group[:4]  # 4 cards in a group
            run_found = True

        # -- partial runs found
        elif ranking:
            red_run_len = len(red_run_group)
            black_run_len = len(black_run_group)

            # add longer run to run_group first
            run_group_len = max(red_run_len, black_run_len)
            run_group = red_run_group if red_run_len == run_group_len \
                else black_run_group

            # remainders
            # -- shorter run's remainder first, then shorter run,
            #       then longer run's remainder
            short_remainder = red_run_remainder if run_group == red_run_group\
                else black_run_remainder
            short_run = red_run_group if run_group == black_run_group \
                else black_run_group
            long_remainder = red_run_remainder if run_group \
                == black_run_group else black_run_remainder

            run_remainder = short_remainder + short_run + long_remainder
            
            run_found = None
        
        # -- no runs found
        else:
            run_remainder = cards

        return run_remainder, run_group, run_found

    def find_set_group(cards):
        set_remainder, set_group, set_found = find_set_phase(cards, 
        phase_type)

        if set_found:
            set_remainder = set_group[4:] + set_remainder
            set_group = set_group[:4]  # 4 cards in a group
            
        return set_remainder, set_group, set_found

    function_order = [[find_run_group, find_set_group],
        [find_set_group, find_run_group]]

    # start by trying to find run group first then set group
    # if unsuccessful, then try finding set group first
    for func_1, func_2 in function_order:
        func_2_complete = False

        # (1) Find 1st group
        func_1_remainder, func_1_group, func_1_complete = func_1(hand)

        # (2*) Find 2nd group - *only if first group found
        if func_1_complete:
            remainder, func_2_group, func_2_complete = \
                func_2(func_1_remainder)
        
        # both groups complete - Phase is Complete
        if func_2_complete:
            # add both groups to phase list
            # -- add run group first, then set group
            if func_1 == find_run_group:
                phase_list[0] = func_1_group
                phase_list[1] = func_2_group
            else:
                phase_list[0] = func_2_group
                phase_list[1] = func_1_group

            phase_complete = True
            
            # break out of phase-finding loop
            break
            
        # 1 complete group found - Partial Phase Found
        elif func_1_complete:
            # add complete group to phase_list
            phase_list[0] = func_1_group

            # add partial group to phase_list
            phase_list[1] = func_2_group

            phase_complete = None

        # no complete groups found
        elif func_1 == find_set_group and phase_list == [[], []]:
            # add partial group to phase_list
            phase_list[0] = func_1_group

            # set remainder and phase_complete flag
            remainder = func_1_remainder
            phase_complete = False
    
    # flatten 2 dimentional phase list to 1 dimentional phase list
    if ranking:
        phase_list = flatten(phase_list)

    return remainder, phase_list, phase_complete

# OTHER HELPER FUNCTIONS
##############################################################################
def flatten(list_2d):
    '''Flattens 2 dimentional list to 1 dimentional list.'''
    list = []
    for group in list_2d:
        for card in group:
            list.append(card)
    return list

def rank(hand, phase_type, phase_on_table, table, player_id):
    '''
    Ranks the hand according to a specific phase.
    Arguments:
        hand(list): list of cards in hand
        phase_type(int): player's current phase
        phase_on_table(bool): True if player has a phase on the table; False
                    otherwise
        table(list): 4-element list of phase plays for each of Players 0—3, 
                    respectively
    Returns:
        ranked_card_list(list): list of cards in hand in order of rank; from
                                highest rank (most wanted) to lowest rank 
                                (least wanted)
        ranks_dict(dict) = dictionary of {card: [ranks], ...}
            -- Ranking Values:
                -- Rank 1: Complete/Partially Complete Phases
                -- Rank 2: Playable to Table
                -- Rank 3: Ultimate Remainders
    '''
    ranks_dict = dd(list)
    phase_complete = False
    ranked_card_list = []

    # Rank 1*: Complete/Partially Complete Phases/Groups
    # -- *if phase not yet played
    # 1a: complete phases
    # 1b: partially complete phases (has at least 1 complete group)
    # 1c*: wild cards (* only for Phases 1, 2, 4 and 5)
    # 1d: partially complete groups
    if not phase_on_table:
        remainder, phase_list, phase_complete = \
            FIND_PHASE_FUNC[phase_type](hand, phase_type)
        
        
        # add Rank 1 cards to `ranked_card_list` and `ranks_dict`
        ranked_card_list += phase_list
        for card in phase_list:
            ranks_dict[card].append(1)
    
    # phase already on table
    else:
        remainder = hand

    # Rank 2*: Cards Playable to Table
    # -- * only if phase is complete
    if phase_on_table or phase_complete:
        if phase_complete:
            # find non-ranking phase
            _, phase_list, phase_complete = \
                    FIND_PHASE_FUNC[phase_type](hand, phase_type, False)

            # add phase to the table (simulate future play)
            table[player_id] = (phase_type, phase_list)

        # Create new remainder list
        # check if multiple cards in hand is playable (to an accumulation)
        playable_to_table, remainder = play_4(table, remainder, True)

        # check if every individual card is playable to the table
        ulti_remainder = []
        for card in remainder:
            card_playable_to_table, remainder = play_4(table, [card], True)
            playable_to_table += card_playable_to_table
            ulti_remainder += remainder

        # add Rank 2 cards to `ranked_card_list` and `ranks_dict`
        ranked_card_list += playable_to_table
        for card in playable_to_table:
            ranks_dict[card].append(2)

    # phase not yet complete
    else:
        playable_to_table = []
        ulti_remainder = remainder
    
    ranked_card_list += playable_to_table
    
    # Rank 3: Ultimate Remainders
    # sort from smallest to largest score value
    ulti_remainder.sort(key=lambda c: SCORE_VALUES[c[VAL]])

    # add ultimate remainders to `ranks_dict`
    for card in ulti_remainder:
        ranks_dict[card].append(3)

    ranked_card_list += ulti_remainder

    return ranks_dict, ranked_card_list

def play_4(table, hand, ranking=False):
    if ranking:
        playable_to_table = []
        remainder = []

    # sort from smallest to largest accumulation
    hand = sorted(hand, key=lambda c: ACC_VALUES[c[VAL]])

    # go through all phases on the table
    for table_player_id in range(len(table)):
        table_phase_type = table[table_player_id][0]
        table_phase_content = table[table_player_id][1]

        # check if player has phase on table
        if table_phase_type:
            for group_num in range(len(table_phase_content)):
                
                next_index = len(table_phase_content[group_num])
                table_group_type = PHASE_GROUPS[table_phase_type][group_num]
                table_group_content = table[table_player_id][1][group_num]

                # group 6/7: 34-accumulation of cards
                if table_group_type in [[6], [6, 7]]:
                    try: 
                        acc_val_list = [ACC_VALUES[c[VAL]] for c in hand]
                        
                        # create new group by adding combinations of cards from 
                        # hand and check if it creates a valid accumulation
                        for r in range(len(hand), 0, -1):

                            for comb in combinations(hand, r):
                                new_group_content = table_group_content[:]
                                new_group_content += list(comb)
                                acc_val_list = [ACC_VALUES[c[VAL]] for c in 
                                                new_group_content]

                                # check if new group is a valid accmumulation
                                if acc_valid(acc_val_list):

                                    # group 7 also needs to be same colour
                                    if table_group_type == [6, 7] and \
                                        not colour_check(new_group_content,
                                         True):
                                        continue

                                    card = comb[0]

                                    if ranking: 
                                        playable_to_table += comb
                                        raise StopIteration

                                    else:
                                        return (4, (card, (table_player_id, 
                                                            group_num, 
                                                            next_index)))
                    except StopIteration:
                        break

                # group 1/3: cards of the same value
                elif table_group_type in [[1], [3]]:
                    val_list = []
                    for card in table_group_content:
                        if card not in WILDS:
                            val_list.append(card[VAL])
                    for card in hand:
                        new_group_content = table_group_content[:]
                        new_group_content.append(card)
                        if card[VAL] in val_list or card in WILDS:
                            if ranking:
                                playable_to_table.append(card)
                                break
                            else:
                                return (4, (card, (table_player_id, group_num, 
                                                    next_index)))
                
                # group 2: cards of the same suit
                elif table_group_type == [2]:
                    suit_list = []
                    for card in table_group_content:
                        if card not in WILDS:
                            suit_list.append(card[SUIT])
                    for card in hand:
                        new_group_content = table_group_content[:]
                        new_group_content.append(card)
                        if card[SUIT] in suit_list or card in WILDS:
                            if ranking:
                                playable_to_table.append(card)
                                break
                            else:
                                return (4, (card, (table_player_id, group_num, 
                                                    next_index)))
                
                # group 4/5: run of cards
                elif table_group_type in [[4], [5]] \
                    and len(table_group_content) < MAX_RUN_LEN:

                    # add each card to the front/back and check if valid run
                    for index in [0, next_index]:
                        for card in hand:
                            new_group_content = table_group_content[:]
                            new_group_content.insert(index, card)

                            if card not in table_group_content \
                                and run_check(new_group_content, MAX_WILDS):

                                # group 5 also needs to be same colour
                                if table_group_type == [5] \
                                    and not colour_check(new_group_content):
                                    break
                                
                                else:
                                    if ranking:
                                        playable_to_table.append(card)
                                        break
                                    else:
                                        return (4, (card, (table_player_id, 
                                                            group_num, index)))
        
        if ranking and playable_to_table:
            playable_to_table_copy = playable_to_table[:]
            for card in hand:
                if card in playable_to_table_copy:
                    playable_to_table_copy.remove(card)
                else:
                    remainder.append(card)
            return playable_to_table, remainder

    if ranking:
        remainder = hand
        return playable_to_table, remainder

    # no table plays
    return False


FIND_PHASE_FUNC = {1: find_set_phase, 2: find_set_phase, 3: find_acc_phase, 
              4: find_set_phase, 5: find_run_phase, 6: find_acc_phase,
              7: find_phase_7}  # {phase: function to find that phase}

# MAIN FUNCTION
##############################################################################
def phazed_play(player_id, table, turn_history, phase_status, hand, 
    discard):

    '''Return a 2-tuple describing the single play your player wishes to make, 
    made up of a play ID and associated play content'''
    if turn_history:
        # prevent magic numbers when indexing
        prev_turn_i, prev_plays_i, prev_play_i = -1, -1, -1
        prev_play = turn_history[prev_turn_i][prev_plays_i][prev_play_i]
        (prev_play_type, _) = prev_play
    else:
        prev_play_type = None

    phase_type = phase_status[player_id] + 1
    phase_on_table = False if table[player_id] in [(None, []), [None, []]] \
                            else True

    # PLAY TYPE 1 OR 2 (PICK-UP PLAY)
    # -- rank cards to check if discard is useful
    if prev_play_type in PLAY_ORDER[1]:
        hand.insert(0, discard)

        # rank potential hand (hand with discard)
        ranks_dict, ranked_card_list = \
            rank(hand, phase_type, phase_on_table, table, player_id)
        
        # Check if dicard if useful
        # phase not found yet; discard is considered 'not useful' if:
        # -- it is the worst ranked card in the rank list
        # -- it is a remainder card
        if (not phase_on_table) and (discard == ranked_card_list[-1] 
            or (max(ranks_dict[discard]) == 3)):
            return (1, None)
        
        # phase found; discard is considered 'not useful' if:
        # -- it is the worst ranked card in the rank list (largest card)
        elif phase_on_table and discard == ranked_card_list[-1]:
            return (1, None)

        # discard is useful - pick up discard
        else:
            return (2, discard)
    
    # PLAY TYPE 3 (PHASE PLAY)
    elif not phase_on_table and prev_play_type in PLAY_ORDER[3]:
        _, phase_list, phase_complete = FIND_PHASE_FUNC[phase_type](hand,
        phase_type, False)

        # complete phase is found in hand - play the phase
        if phase_complete:
            return (3, (phase_type, phase_list))
        # no phase plays found in hand -go to-> PLAY TYPE 5 (discard)

    # PLAY TYPE 4 (TABLE PLAY)
    elif prev_play_type in PLAY_ORDER[4]:
        play = play_4(table, hand)
        if play:
            return play
        # no table play is found -go to-> PLAY TYPE 5 (discard)

    # PLAY TYPE 5 (DISCARD)
    # -- rank cards
    # -- discard leasts wanted card (lowest rank)
    ranks_dict, ranked_card_list = \
        rank(hand, phase_type, phase_on_table, table, player_id)

    return (5, ranked_card_list[-1])
