from game.players import BasePokerPlayer
from functools import reduce
from itertools import groupby
#     CLUB = 2
#     DIAMOND = 4
#     HEART = 8
#     SPADE = 16

#     SUIT_MAP = {2: "C", 4: "D", 8: "H", 16: "S"}

RANK_MAP = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
}

preflop_strong_hand = {'CACK', 'DADK', 'HAHK', 'SASK', 'CACQ', 'DADQ', 'HAHQ', 'SASQ', 'CACJ', 'DADJ', 'HAHJ', 'SASJ', 'CACT', 'DADT', 'HAHT', 'SAST',
                'CKCQ', 'DKDQ', 'HKHQ', 'SKSQ', 'CKCJ', 'DKDJ', 'HKHJ', 'SKSJ', 'CKCT', 'DKDT', 'HKHT', 'SKST'}
preflop_call3b_hand = {'CACJ', 'DADJ', 'HAHJ', 'SASJ', 'CACT', 'DADT', 'HAHT', 'SAST',
                'CKCQ', 'DKDQ', 'HKHQ', 'SKSQ', 'CKCJ', 'DKDJ', 'HKHJ', 'SKSJ', 'CKCT', 'DKDT', 'HKHT', 'SKST'}



class ProPlayer(
    BasePokerPlayer
):  # Do not forget to make parent class as "BasePokerPlayer"

    #  we define the logic to make an action through this method. (so this method would be the core of your AI)
    def __init__(self):
        # seat = [0: SB, 1: BB]
        # self.seat = 0
        self.score = -1
        self.opponent_action = {'preflop': {'action':'NULL', 'amount':0, 'raise':0}, 'flop': {'action':'NULL', 'amount':0, 'raise':0}, 'turn': {'action':'NULL', 'amount':0, 'raise':0}, 'river': {'action':'NULL', 'amount':0, 'raise':0}}
        # plan = [0: No action, 1: check rasie, 2: delay cbet]
        self.plan = 0
        self.flag = {
                        'one_pair': 0, # 1:bottom, 2:middle, 3:top 
                        'two_pair': 0, # 1:b+m, 2:b+t, 3:m+t
                        'set': 0,      # 1:set(communtiy 2 cards), 2:bottom, 3:middle, 4:top
                        'straight': 0, # 1:gut_shot, 2:open_ended, 3:straight
                        'flush': 0,    # 1:draw, 2:flush(no A), 3:nuts flush 
                        'fullhouse': 0,# 1:fullhouse
                        'quads': 0,    # 1:quads
                        'straight_flush': 0, # 1:straight_flush, 2:royal_straight_flush
                    }
        self.my_last_action = 0
    def preflop_hand_evaluator(self, hand):
        score = RANK_MAP[hand[1]] + RANK_MAP[hand[3]]
        if hand[0] == hand[2]: # suited
            score += 1
        elif hand[1] == hand[3]: # pair
            score += 4
        if score >= 26: # AJs+, JJ+
            return 3
        elif score >= 20: # T9s+, 88+
            return 2
        elif score >= 13:
            return 1
        else:
            return 0
    def flop_hand_evaluator(self, hand, community_hand):
        self.flag['quads'] = self.is_quads(hand, community_hand)
        self.flag['fullhouse'] = self.is_fullhouse(hand, community_hand)
        self.flag['flush'] = self.is_flush(hand, community_hand)
        self.flag['straight'] = self.is_straight(hand, community_hand)
        self.flag['set'] = self.is_set(hand, community_hand)
        self.flag['two_pair'] = self.is_twopair(hand, community_hand)
        self.flag['one_pair'] = self.is_onepair(hand, community_hand)
        # straight flush
        if self.flag['straight'] == 3:
            if self.flag['flush'] == 2:
                self.flag['straight_flush'] = 1
            elif self.flag['flush'] == 3:
                self.flag['straight_flush'] = 2
            
        if self.flag['straight_flush'] >= 1 or self.flag['quads'] == 1 or self.flag['fullhouse'] >= 1 or self.flag['flush'] >= 2 or self.flag['straight'] == 3:
            return 5
        elif self.flag['set'] >= 2 or self.flag['two_pair'] >= 2:
            return 4
        elif self.flag['set'] == 1 or self.flag['two_pair'] == 1 or (self.flag['straight'] >= 1 and self.flag['flush'] == 1):
            return 3
        elif self.flag['straight'] == 2 or self.flag['flush'] == 1 or self.flag['one_pair'] == 3:
            return 2
        elif self.flag['straight'] == 1 or self.flag['one_pair'] == 2:
            return 1
        else:
            return 0  
    def turn_hand_evaluator(self, hand, community_hand):
        self.flag['quads'] = self.is_quads(hand, community_hand)
        self.flag['fullhouse'] = self.is_fullhouse(hand, community_hand)
        self.flag['flush'] = self.is_flush(hand, community_hand)
        self.flag['straight'] = self.is_straight(hand, community_hand)
        self.flag['set'] = self.is_set(hand, community_hand)
        self.flag['two_pair'] = self.is_twopair(hand, community_hand)
        self.flag['one_pair'] = self.is_onepair(hand, community_hand)
        # straight flush
        if self.flag['straight'] == 3:
            if self.flag['flush'] == 2:
                self.flag['straight_flush'] = 1
            elif self.flag['flush'] == 3:
                self.flag['straight_flush'] = 2
            
        if self.flag['straight_flush'] >= 1 or self.flag['quads'] == 1 or self.flag['fullhouse'] >= 1 or self.flag['flush'] >= 2 or self.flag['straight'] == 3:
            return 5
        elif self.flag['set'] >= 2 or self.flag['two_pair'] >= 2:
            return 4
        elif self.flag['set'] == 1 or self.flag['two_pair'] == 1:
            return 3
        elif self.flag['one_pair'] == 3 or (self.flag['straight'] >= 1 and self.flag['flush'] == 1):
            return 2
        elif self.flag['straight'] == 2 or self.flag['flush'] == 1:
            return 1
        else:
            return 0
    def river_hand_evaluator(self, hand, community_hand):
        self.flag['quads'] = self.is_quads(hand, community_hand)
        self.flag['fullhouse'] = self.is_fullhouse(hand, community_hand)
        self.flag['flush'] = self.is_flush(hand, community_hand)
        self.flag['straight'] = self.is_straight(hand, community_hand)
        self.flag['set'] = self.is_set(hand, community_hand)
        self.flag['two_pair'] = self.is_twopair(hand, community_hand)
        self.flag['one_pair'] = self.is_onepair(hand, community_hand)
        # straight flush
        if self.flag['straight'] == 3:
            if self.flag['flush'] == 2:
                self.flag['straight_flush'] = 1
            elif self.flag['flush'] == 3:
                self.flag['straight_flush'] = 2
            
        if self.flag['straight_flush'] >= 1 or self.flag['quads'] == 1 or self.flag['fullhouse'] >= 1 or self.flag['flush'] >= 2:
            return 6
        elif self.flag['straight'] == 3:
            return 5
        elif self.flag['set'] > 1:
            return 4
        elif self.flag['set'] == 1:
            return 3
        elif self.flag['two_pair'] >= 1:
            return 2
        elif self.flag['one_pair'] == 3:
            return 1
        else:
            return 0

    def preflop_action(self, valid_actions, hole_card, round_state):
        if self.score == -1:
            hand = hole_card[0] + hole_card[1]
            self.score = self.preflop_hand_evaluator(hand)
        
        if self.opponent_action['preflop']['action'] == 'raise':
            self.opponent_action['preflop']['raise'] += 1
            if self.score == 3:
                raise_action_info = valid_actions[2]
                action = raise_action_info['action']
                self.my_last_action = 2
                if raise_action_info['amount']['min'] == -1:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
                    self.my_last_action = 1 
                    return action, amount
                amount = min(self.stack, 2 * raise_action_info['amount']['min'], raise_action_info['amount']['max'])
            elif self.score == 2 and self.opponent_action['preflop']['raise'] <= 1:
                if self.opponent_action['preflop']['amount'] >= 10 * round_state['small_blind_amount']:
                    fold_action_info = valid_actions[0]
                    action, amount = fold_action_info['action'], fold_action_info['amount']
                    self.my_last_action = 0
                else:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
                    self.my_last_action = 1
            else:
                fold_action_info = valid_actions[0]
                action, amount = fold_action_info['action'], fold_action_info['amount']
                self.my_last_action = 0 
        else: # opponent call or myplayer act first 
            if self.score == 0:
                fold_action_info = valid_actions[0]
                action, amount = fold_action_info['action'], fold_action_info['amount']
            elif self.score == 1:
                call_action_info = valid_actions[1]
                action, amount = call_action_info["action"], call_action_info["amount"]
                self.my_last_action = 1
            else:
                raise_action_info = valid_actions[2]
                action = raise_action_info['action']
                self.my_last_action = 2
                amount = min(self.stack, 2 * raise_action_info['amount']['min'], raise_action_info['amount']['max'])

        return action, amount    
    def flop_action(self,  valid_actions, hole_card, round_state):
        if self.score == -1:
            self.score = self.flop_hand_evaluator(hole_card, round_state['community_hand'])
        
        if self.opponent_action['flop']['action'] == 'raise':
            self.opponent_action['flop']['raise'] += 1
            if self.my_last_action == 2: # opponent donk or reraise
                if self.score >= 4:
                    raise_action_info = valid_actions[2]
                    action = raise_action_info['action']
                    self.my_last_action = 2
                    if raise_action_info['amount']['min'] == -1:
                        call_action_info = valid_actions[1]
                        action, amount = call_action_info["action"], call_action_info["amount"]
                        self.my_last_action = 1 
                        return action, amount
                    amount = min(self.stack, 2 * raise_action_info['amount']['min'], raise_action_info['amount']['max'])
                elif self.score == 3:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
                    self.my_last_action = 1
                elif self.score == 2 and self.opponent_action['flop']['amount'] <=  3 * round_state['pot']['main']['amount'] / 5:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
                    self.my_last_action = 1
                else:
                    fold_action_info = valid_actions[0]
                    action, amount = fold_action_info['action'], fold_action_info['amount']
            else:   # opponent cbet or lead
                if self.score == 3: 
                    if self.opponent_action['flop']['amount'] <= round_state['pot']['main']['amount'] / 3 and self.opponent_action['flop']['raise'] <= 1:
                        raise_action_info = valid_actions[2]
                        action = raise_action_info['action']
                        self.my_last_action = 2
                        if raise_action_info['amount']['min'] == -1:
                            call_action_info = valid_actions[1]
                            action, amount = call_action_info["action"], call_action_info["amount"]
                            self.my_last_action = 1 
                            return action, amount
                        amount = min(self.stack, 2 * raise_action_info['amount']['min'], raise_action_info['amount']['max'])
                    else:
                        call_action_info = valid_actions[1]
                        action, amount = call_action_info["action"], call_action_info["amount"]
                        self.my_last_action = 1
                elif self.score >= 4 or self.score == 2:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
                    self.my_last_action = 1
                else:
                    fold_action_info = valid_actions[0]
                    action, amount = fold_action_info['action'], fold_action_info['amount']
        else:
            if self.my_last_action == 2 or self.score == 5 or self.score == 2:
                raise_action_info = valid_actions[2]
                action = raise_action_info['action']
                self.my_last_action = 2
                if raise_action_info['amount']['min'] == -1:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
                    self.my_last_action = 1 
                    return action, amount
                if round_state['pot']['main']['amount']/3 >= raise_action_info['amount']['min']:
                    amount = min(self.stack, round_state['pot']['main']['amount']/3, raise_action_info['amount']['max'])
                else:
                    amount = min(self.stack, raise_action_info['amount']['min'])
            elif self.score == 4 or self.score == 3:
                raise_action_info = valid_actions[2]
                action = raise_action_info['action']
                self.my_last_action = 2
                if raise_action_info['amount']['min'] == -1:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
                    self.my_last_action = 1 
                    return action, amount
                if round_state['pot']['main']['amount']/2 >= raise_action_info['amount']['min']:
                    amount = min(self.stack, round_state['pot']['main']['amount']/2, raise_action_info['amount']['max'])
                else:
                    amount = min(self.stack, raise_action_info['amount']['min'])
            else:
                call_action_info = valid_actions[1]
                action, amount = call_action_info["action"], call_action_info["amount"]
                self.my_last_action = 1

        return action, amount 
    def turn_action(self,  valid_actions, hole_card, round_state):
        if self.score == -1:
            self.score = self.turn_hand_evaluator(hole_card, round_state['community_hand'])
        
        if self.opponent_action['turn']['action'] == 'raise':
            self.opponent_action['turn']['raise'] += 1
            if self.score >= 4:
                raise_action_info = valid_actions[2]
                action = raise_action_info['action']
                self.my_last_action = 2
                if raise_action_info['amount']['min'] == -1:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
                    self.my_last_action = 1 
                    return action, amount
                amount = min(self.stack, 2 * raise_action_info['amount']['min'], raise_action_info['amount']['max'])
            elif self.score == 3:
                call_action_info = valid_actions[1]
                action, amount = call_action_info["action"], call_action_info["amount"]
                self.my_last_action = 1
            elif self.score == 2 and self.opponent_action['flop']['amount'] <=  round_state['pot']['main']['amount'] / 3:
                call_action_info = valid_actions[1]
                action, amount = call_action_info["action"], call_action_info["amount"]
                self.my_last_action = 1
            else:
                fold_action_info = valid_actions[0]
                action, amount = fold_action_info['action'], fold_action_info['amount']
        else:
            if self.my_last_action == 2 or (self.score <= 4 and self.score >= 2):
                raise_action_info = valid_actions[2]
                action = raise_action_info['action']
                self.my_last_action = 2
                if raise_action_info['amount']['min'] == -1:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
                    self.my_last_action = 1 
                    return action, amount
                if round_state['pot']['main']['amount']/2 >= raise_action_info['amount']['min']:
                    amount = min(self.stack, round_state['pot']['main']['amount']/2, raise_action_info['amount']['max'])
                else:
                    amount = min(self.stack, raise_action_info['amount']['min'])
            else:
                call_action_info = valid_actions[1]
                action, amount = call_action_info["action"], call_action_info["amount"]
                self.my_last_action = 1

        return action, amount
    def river_action(self, valid_actions, hole_card, round_state):
        if self.score == -1:
            self.score = self.river_hand_evaluator(hole_card, round_state['community_hand'])
        
        raise_times = self.opponent_action['preflop']['raise'] + self.opponent_action['flop']['raise'] + self.opponent_action['turn']['raise'] + 3 * self.opponent_action['river']['raise']
        if self.opponent_action['river']['action'] == 'raise':
            self.opponent_action['river']['raise'] += 1
            if self.score == 6:
                raise_action_info = valid_actions[2]
                action = raise_action_info['action']
                self.my_last_action = 2
                if raise_action_info['amount']['min'] == -1:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
                    self.my_last_action = 1 
                    return action, amount
                amount = min(self.stack, 2 * raise_action_info['amount']['min'], raise_action_info['amount']['max'])
            elif self.score >= 4:
                call_action_info = valid_actions[1]
                action, amount = call_action_info["action"], call_action_info["amount"]
                self.my_last_action = 1
            elif self.score >= 2 and raise_times <= 3:
                call_action_info = valid_actions[1]
                action, amount = call_action_info["action"], call_action_info["amount"]
                self.my_last_action = 1
            else:
                fold_action_info = valid_actions[0]
                action, amount = fold_action_info['action'], fold_action_info['amount']
        else:
            if self.my_last_action == 2:
                if self.score >= 5 or (self.score == 4 and raise_times < 3) or (self.score == 0 and raise_times < 3):
                    raise_action_info = valid_actions[2]
                    action = raise_action_info['action']
                    self.my_last_action = 2
                    if raise_action_info['amount']['min'] == -1:
                        call_action_info = valid_actions[1]
                        action, amount = call_action_info["action"], call_action_info["amount"]
                        self.my_last_action = 1 
                        return action, amount
                    if 2*round_state['pot']['main']['amount']/3 >= raise_action_info['amount']['min']:
                        amount = min(self.stack, 2*round_state['pot']['main']['amount']/3, raise_action_info['amount']['max'])
                    else:
                        amount = min(self.stack, raise_action_info['amount']['min'])
                else:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
                    self.my_last_action = 1
            else:
                if self.score >= 5:
                    raise_action_info = valid_actions[2]
                    action = raise_action_info['action']
                    self.my_last_action = 2
                    if raise_action_info['amount']['min'] == -1:
                        call_action_info = valid_actions[1]
                        action, amount = call_action_info["action"], call_action_info["amount"]
                        self.my_last_action = 1 
                        return action, amount
                    if round_state['pot']['main']['amount'] >= raise_action_info['amount']['min']:
                        amount = min(self.stack, round_state['pot']['main']['amount'], raise_action_info['amount']['max'])
                    else:
                        amount = min(self.stack, raise_action_info['amount']['min'])
                else:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
                    self.my_last_action = 1

        return action, amount
    def declare_action(self, valid_actions, hole_card, round_state):
        if round_state['street'] == 'preflop':
            action, amount = self.preflop_action(valid_actions, hole_card, round_state)
        elif round_state['street'] == 'flop':
            action, amount = self.flop_action(valid_actions, hole_card, round_state)
        elif round_state['street'] == 'turn':
            action, amount = self.turn_action(valid_actions, hole_card, round_state)
        elif round_state['street'] == 'river':
            action, amount = self.river_action(valid_actions, hole_card, round_state)
        
        # valid_actions format => [fold_action_info, call_action_info, raise_action_info]
        # call_action_info = valid_actions[1]
        # action, amount = call_action_info["action"], call_action_info["amount"]
        return action, amount  # action returned here is sent to the poker engine

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        self.my_last_action = 0
        pass

    def receive_street_start_message(self, street, round_state):
        self.score = -1
        pass

    def receive_game_update_message(self, action, round_state):
        if action['player_uuid'] != self.uuid:
            self.opponent_action[round_state['street']]['action'] = action['action']
            self.opponent_action[round_state['street']]['amount'] = action['amount']

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass

    def is_onepair(self, hole, community_hand):
        ranks = sorted([card.rank for card in community_hand])
        len = len(ranks)
        if hole[0].rank == hole[1].rank:
            if hole[0].rank > ranks[0]:
                return 3
            elif hole[0].rank < ranks[len-1]:
                return 1
            else:
                return 2
        for card in hole:
            for com_card in community_hand:
                if card.rank == com_card.rank:
                    if card.rank == ranks[0]:
                        return 3
                    elif card.rank == ranks[len-1]:
                        return 1
                    else:
                        return 2
        
        return 0
    def is_twopair(self, hole, community_hand):
        ranks = sorted([card.rank for card in community_hand])
        len = len(ranks)
        count = 0
        pair_ranks = []
        memo = 0
        for card in community_hand:
            mask = 1 << card.rank
            if memo & mask != 0:
                pair_ranks.append(card.rank)
                count += 1
            memo |= mask

        if hole[0].rank == hole[1].rank:
            pair_ranks.append(hole[0].rank)
            count += 1
            pair_ranks = sorted(pair_ranks)
            if count >= 2:
                if hole[0].rank >= pair_ranks[1]:
                    if len(pair_ranks) == 2 or hole[0].rank > ranks[0]:
                        return 3
                    elif hole[0].rank < ranks[0]:
                        return 2
                    else:
                        return 1 
        else:
            for h_card in hole:
                memo = 1 << h_card.rank
                for c_card in community_hand:
                    mask = 1 << c_card.rank
                    if memo & mask != 0:
                        pair_ranks.append(card.rank)
                        count += 1
            pair_ranks = sorted(pair_ranks)
            if count == 3:
                if hole[0].rank == pair_ranks[2] or hole[1].rank == pair_ranks[2]:
                    return 2
                else:
                    return 3
            elif count == 2:
                return 3
            
        return 0
    def is_set(self, hole, community_hand):
        ranks = sorted([card.rank for card in community_hand])
        cards = hole + community_hand
        rank = -1
        bit_memo = reduce(
            lambda memo, card: memo + (1 << (card.rank - 1) * 3), cards, 0
        )
        for r in range(2, 15):
            bit_memo >>= 3
            count = bit_memo & 7
            if count >= 3:
                rank = r
        if rank != hole[0].rank and rank != hole[0].rank:
            return 0
        elif rank == hole[0].rank and rank == hole[0].rank:
            if rank == ranks[0]:
                return 4
            elif rank == ranks[1]:
                return 3
            else:
                return 2
        else:
            return 1
    def is_quads(self, hole, community_hand):
        cards = hole + community_hand
        fetch_rank = lambda card: card.rank
        for rank, group_obj in groupby(sorted(cards, key=fetch_rank), key=fetch_rank):
            g = list(group_obj)
            if len(g) >= 4:
                return 1
        return 0
    def is_flush(self, hole, community_hand):
        cards = hole + community_hand
        best_suit_rank = -1
        fetch_suit = lambda card: card.suit
        fetch_rank = lambda card: card.rank
        return_value = 0
        for suit, group_obj in groupby(sorted(cards, key=fetch_suit), key=fetch_suit):
            g = list(group_obj)
            if len(g) >= 5:
                max_rank_card = max(g, key=fetch_rank)
                best_suit_rank = max(best_suit_rank, max_rank_card.rank)
                if max_rank_card == 14:
                    return_value = 3
                else:
                    return_value = 2    
            elif len(g) == 4:
                return_value = 1

        return return_value
    def is_straight(self, hole, community_hand):
        cards = hole + community_hand
        bit_memo = reduce(lambda memo, card: memo | 1 << card.rank, cards, 0)
        rank = -1
        straight_check = lambda acc, i: acc & (bit_memo >> (r + i) & 1) == 1
        return_value = 0
        for r in range(2, 15):
            if reduce(straight_check, range(5), True):
                return_value = 3
            elif reduce(straight_check, range(4), True):
                return_value = 2
            
        return return_value
    def is_fullhouse(self, hole, community_hand):
        cards = hole + community_hand
        fetch_rank = lambda card: card.rank
        three_card_ranks, two_pair_ranks = [], []
        for rank, group_obj in groupby(sorted(cards, key=fetch_rank), key=fetch_rank):
            g = list(group_obj)
            if len(g) >= 3:
                three_card_ranks.append(rank)
            if len(g) >= 2:
                two_pair_ranks.append(rank)
        two_pair_ranks = [
            rank for rank in two_pair_ranks if not rank in three_card_ranks
        ]
        if len(three_card_ranks) == 2:
            two_pair_ranks.append(min(three_card_ranks))
        max_ = lambda l: None if len(l) == 0 else max(l)
        if max_(three_card_ranks) > 0 and max_(two_pair_ranks) > 0:
            return 1
        else:
            return 0  
def setup_ai():
    return ProPlayer()