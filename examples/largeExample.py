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

def colour_check(group, aces_check=False):
    '''
    Checks if a group of cards is all of the same colour.

    Parameters
    ----------
    group : list
        A list of cards.
    aces_check : bool
        Whether or not to check for the presence of aces.

    Returns
    -------
    bool
        Whether or not the group is of the same colour.

    Examples
    --------
    >>> colour_check(['2H', '5H', '8H'])
    True

    '''
    num_cards = len(group)
    colour_dict = dd(int)

    for card in group:
        if card in WILDS and not aces_check:
            colour_dict['wilds'] += 1
        else:
            colour_dict[COLOUR[card[SUIT]]] += 1
            
    if colour_dict['red'] + colour_dict['wilds'] == num_cards \
        or colour_dict['black'] + colour_dict['wilds'] == num_cards:
        return True

    return False

def run_check(group, max_wild, ref='', wild_count=0):
    '''
    Check if a group of cards is a run.

    Parameters
    ----------
    group : list
        The group of cards to be checked.
    max_wild : int
        The maximum number of wilds allowed in the run.
    ref : str, optional
        The value of the card that the run should start with. Defaults to ''.
    wild_count : int, optional
        The number of wilds in the run. Defaults to 0.

    Returns
    -------
    bool
        True if the group is a run, False otherwise.

    Examples
    --------
    >>> run_check(['2C', '3C', '4C', '5C', '6C'], 0)
    True
    >>> run_check(['2C', '3C', '4C', '5C', '6C'], 1)
    True
    >>> run_check(['2C', '3C', '4C', '5C', '6C'], 2)
    True
    >>> run_check(
    '''
    if wild_count > max_wild:
        return False

    elif not group:
        return True

    elif group[0] in WILDS:
        return run_check(group[1:], max_wild,
            RUN_ORDER[RUN_ORDER.index(ref) + 1], wild_count + 1)

    elif group[0][VAL] == ref or ref == '':
        return run_check(group[1:], max_wild,
            RUN_ORDER[RUN_ORDER.index(group[0][VAL]) + 1], wild_count)

    return False

def acc_valid(val_list, acc_total=0, acc_list=ACC_TOTALS):
    '''
    Validate a given accumulative total against a given list of accumulative totals.

    Parameters
    ----------
    val_list : list
        The list of values to be summed.
    acc_total : int
        The current accumulative total.
    acc_list : list
        The list of accumulative totals.

    Returns
    -------
    bool
        Whether or not the given accumulative total is valid against the given list of accumulative totals.

    Examples
    --------
    >>> acc_valid([1, 2, 3], 0, [3, 4, 5])
    True

    '''
    if not acc_list or acc_total > acc_list[0]:
        return False
    elif not val_list and acc_total == acc_list[0]:
        return True
    elif not val_list and acc_total < acc_list[0]:
        return None
    elif acc_total == acc_list[0]:
        return acc_valid(val_list[1:], acc_total + val_list[0], acc_list[1:])
    elif acc_total < acc_list[0]:
        return acc_valid(val_list[1:], acc_total + val_list[0], acc_list)


def find_set_phase(hand, phase_type, ranking=True):
    '''
    Finds the best set(s) of cards to play for a given phase.

    Parameters
    ----------
    hand : list
        The player's hand.
    phase_type : int
        The phase type.
    ranking : bool, optional
        Whether or not to rank the set(s) of cards by score.

    Returns
    -------
    list
        The remainder of the player's hand.
    list
        The set(s) of cards to play.
    bool
        Whether or not the set(s) of cards are complete.

    Examples
    --------
    >>> find_set_phase(['3C', '3D', '3H', '3S', '4C', '4D', '4H', '4S', '7C', 
    ...                 '7D', '7H', '7S', '8C', '8D', '8H', '8S', 'AC', 'AD', 
    ...                 'AH', 'AS', 'JC', 'JD', 'JH', 'JS', 'KC', 'KD', 'KH', 
    ...                 'KS', 'QC', 'QD', 'QH', 'QS'], 1)
    (['3C', '3D', '3H', '3S', '4C', '4D', '4H', '4S', '7C', '7D', '7H', '7S', 
      '8C', '8D', '8H', '8S', 'AC', 'AD', 'AH', 'AS', 'JC', 'JD', 'JH', 'JS', 
      'KC', 'KD', 'KH', 'KS', 'QC', 'QD', 'QH', 'QS'], 
     ['3C', '3D', '3H', '3S', '4C', '4D', '4H', '4S', '7C', '7D', '7H', '7S', 
      '8C', '8D', '8H', '8S', 'AC', 'AD', 'AH', 'AS', 'JC', 'JD', 'JH', 'JS', 
      'KC', 'KD', 'KH', 'KS', 'QC', 'QD', 'QH', 'QS'], 
     False)

    '''
    def find_partial_sets(freq_dict):
        '''
        Finds partial sets.

        Parameters
        ----------
        freq_dict : dict
            A dictionary of card values and their frequencies.

        Returns
        -------
        list
            A list of partial sets.
        list
            A list of remaining cards.

        Examples
        --------
        >>> find_partial_sets({'A': 4, '2': 2, '3': 2, '4': 2, '5': 1})
        [['A', 'A', 'A', 'A'], ['2', '2', '2', '5'], ['3', '3', '4', '4']]
        [['5']]
    
        '''
        lengths_list = [len(card_list) for card_list in 
            list(freq_dict.values())]
        lowest_freq = min(lengths_list)

        remainder = []
        partials = []
        scores_dict = dd(int)

        for key, card_list in list(freq_dict.items()):
            if len(card_list) == lowest_freq:
                freq_dict.pop(key)
                remainder += card_list
            else:
                total_score_val = 0
                for card in card_list:
                    total_score_val += SCORE_VALUES[card[VAL]]
                scores_dict[key] = total_score_val
        partial_item_list = sorted(list(freq_dict.items()), key=lambda item: 
                                    (-len(item[1]), scores_dict[item[0]]))
        for key, card_group in partial_item_list:
            card_group.sort(key=lambda c: SCORE_VALUES[c[VAL]])
            for card in card_group:
                partials.append(card)

        return partials, remainder
    
    phase_dict = {1: [3, 2, VAL], 2: [7, 1, SUIT], 4: [4, 2, VAL], 
                  7: [4, 1, VAL]}
    group_len = phase_dict[phase_type][0]
    phase_len = phase_dict[phase_type][1]
    mode  = phase_dict[phase_type][2]
    hand.sort(key=lambda c: -ACC_VALUES[c[VAL]])

    freq_dict = dd(list)
    for card in hand:
        if card in WILDS:
            freq_dict['wild'].append(card)
        else:
            key = ACC_VALUES[card[VAL]] if mode == VAL else card[SUIT]
            freq_dict[key].append(card)
    
    phase_list = []
    remainder = []

    for key, card_list in list(freq_dict.items())[:]:
        if len(phase_list) == phase_len:
            break
        elif key!='wild' and len(card_list) >= group_len:
            phase_list.append(card_list[:group_len])
            freq_dict[key] = card_list[group_len:]

    for key, card_list in list(freq_dict.items())[:]:
        if len(phase_list) == phase_len:
            break
        elif key != 'wild' and len(card_list) >= MIN_NATURAL \
            and len(card_list) + len(freq_dict['wild']) >= group_len \
                and len(phase_list) < phase_len:
            new_card_list = card_list + freq_dict['wild'][:group_len
                - len(card_list)]
            phase_list.append(new_card_list)
            freq_dict['wild'] = freq_dict['wild'][group_len - len(card_list):]
            freq_dict.pop(key)
    if len(phase_list) == phase_len:
        phase_complete = True
    elif 0 < len(phase_list) < phase_len:
        phase_complete = None
    else:
        phase_complete = False
    if not ranking:
        if phase_complete:
            remainder = flatten(list(freq_dict.values()))
        else:
            remainder = hand
    else: 
        phase_list = flatten(phase_list)
        for key, _ in list(freq_dict.items())[:]:
            if key == 'wild' and freq_dict[key]:
                phase_list += freq_dict[key]
                freq_dict.pop('wild')
            elif not freq_dict[key]:
                freq_dict.pop(key)
        if freq_dict:
            partial_set_cards, remainder = find_partial_sets(freq_dict)
            phase_list += partial_set_cards

    return remainder, phase_list, phase_complete

def find_acc_phase(hand, phase_type, ranking=True):
    '''
    Finds the best possible set of cards to play in a trick.

    Parameters
    ----------
    cards : list
        The cards you have available to play in the trick.
    mode : str
        The mode of play.

    Returns
    -------
    tuple
        A tuple containing 3 lists:
            - The list of cards to play in the trick.
            - The list of cards not played in the trick.
            - The list of cards to save for a later trick.

    Examples
    --------
    >>> find_acc_group([('H', 'A'), ('H', 'K'), ('H', 'Q'), ('H', 'J'), ('H', '10'), ('H', '9')], 'short')
    ([('H', 'A'), ('H', 'K'), ('H', 'Q'), ('H', 'J')], [('H', '10'), ('H', '9')], [])

    '''
    def find_acc_group(cards, mode):
        '''
        Finds the best possible set of cards to play in a trick.

        Parameters
        ----------
        cards : list
            The cards you have available to play in the trick.
        mode : str
            The mode of play.

        Returns
        -------
        tuple
            A tuple containing 3 lists:
                - The list of cards to play in the trick.
                - The list of cards not played in the trick.
                - The list of cards to save for a later trick.

        Examples
        --------
        >>> find_acc_group([('H', 'A'), ('H', 'K'), ('H', 'Q'), ('H', 'J'), ('H', '10'), ('H', '9')], 'short')
        ([('H', 'A'), ('H', 'K'), ('H', 'Q'), ('H', 'J')], [('H', '10'), ('H', '9')], [])
    
        '''
        shortest = 3
        longest = min(8, len(cards))

        if mode == 'short':
            combination_sizes = range(shortest, longest)
        else:
            combination_sizes = range(longest, shortest - 1, -1)

        cards.sort(key=lambda c: ACC_VALUES[c[VAL]])

        group_found = False
        acc_group = []
        group_remainder = []
        promising_diff = 0

        for r in combination_sizes:
            try:
                for comb in combinations(cards, r):
                    acc_values = [ACC_VALUES[card[VAL]] for card in comb]
                    difference = sum(acc_values) - ACC_TOTALS[0]
                    if not difference:

                        if group_type == 7:
                            if not colour_check(comb, True):
                                continue

                        acc_group = list(comb)
                        group_found = True

                        raise StopIteration
                    elif difference <= promising_diff:
                        acc_group = list(comb)
            except StopIteration:
                break
        group_remainder = []
        for card in cards:
            if card not in acc_group:
                group_remainder.append(card)

        return group_found, group_remainder, acc_group

    phase_dict = {3: 6, 6: 7}
    group_type = phase_dict[phase_type]

    phase_list = []
    modes_list = ['long', 'short']
    for mode in modes_list:
        group_2_found = False

        group_1_found, group_1_remainder, group_1 = find_acc_group(hand, mode)

        if group_1_found:
            group_2_found, remainder, group_2 = \
                find_acc_group(group_1_remainder, 'long')

        if group_2_found:
            phase_list.append(group_1)
            phase_list.append(group_2)

            phase_complete = True
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
    remainder = []
    phase_list = [[], []]

    def find_run_group(cards):

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
