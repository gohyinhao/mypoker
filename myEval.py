class evalFunction(object):

    def __init__(self, hole_cards, community_cards, current_street, weights):
        self.hole_cards = hole_cards
        self.community_cards = community_cards
        self.current_street = current_street
        self.weights = weights

    def baseValue(self):
        if self.hole_cards[0][1] == 'A':
            value1 = 14
        elif self.hole_cards[0][1] == 'K':
            value1 = 13
        elif self.hole_cards[0][1] == 'Q':
            value1 = 12
        elif self.hole_cards[0][1] == 'J':
            value1 = 11
        elif self.hole_cards[0][1] == 'T':
            value1 = 10
        else:
            value1 = int(self.hole_cards[0][1])

        if self.hole_cards[1][1] == 'A':
            value2 = 14
        elif self.hole_cards[1][1] == 'K':
            value2 = 13
        elif self.hole_cards[1][1] == 'Q':
            value2 = 12
        elif self.hole_cards[1][1] == 'J':
            value2 = 11
        elif self.hole_cards[1][1] == 'T':
            value2 = 10
        else:
            value2 = int(self.hole_cards[1][1])

        if value1 > value2:
            highCard = value1
            lowCard = value2
        else:
            highCard = value2
            lowCard = value1

        # Raise pocket 8s and above, Call otherwise
        if highCard == lowCard:
            if highCard >= 8:
                baseValue = 1
            else:
                baseValue = 0
        # Raise if total value is above 14 or connected, Call otherwise
        elif (highCard + lowCard) >= 14 or (highCard-1) == lowCard:
            baseValue = 1
        else:
            baseValue = 0

        return self.weights[0] * baseValue

    def pairValue(self):
        pairValue = 0

        def cardValue(card):
            if card[1] == 'A':
                value = 14
            elif card[1] == 'K':
                value = 13
            elif card[1] == 'Q':
                value = 12
            elif card[1] == 'J':
                value = 11
            elif card[1] == 'T':
                value = 10
            else:
                value = int(card[1])
            return value

        # Count number of community cards that are the same as your hand
        for cards in self.community_cards:
            if cards[1] == self.hole_cards[0][1] or cards[1] == self.hole_cards[1][1]:
                pairValue = pairValue + cardValue(cards)
            else:
                pairValue = pairValue - cardValue(cards)

        # Higher value if pocket pair
        if self.hole_cards[0][1] == self.hole_cards[1][1]:
            pairValue = pairValue * 2

        return self.weights[1] * pairValue

    def flushValue(self):

        def cardValue(card):
            if card[1] == 'A':
                value = 14
            elif card[1] == 'K':
                value = 13
            elif card[1] == 'Q':
                value = 12
            elif card[1] == 'J':
                value = 11
            elif card[1] == 'T':
                value = 10
            else:
                value = int(card[1])
            return value

        # Minimum number of cards that must be suited for a possibility for a flush
        if self.current_street == "preflop":
            minSuits = 10000
        if self.current_street == "flop":
            minSuits = 3
        if self.current_street == "turn":
            minSuits = 4
        if self.current_street == "river" or self.current_street == "showdown":
            minSuits = 5

        # Count number of suited cards for each suit
        countD = countC = countH = countS = flushValue = 0
        combinedCards = self.hole_cards + self.community_cards
        for card in combinedCards:
            if card[0] == 'D':
                countD = countD + 1
            if card[0] == 'C':
                countC = countC + 1
            if card[0] == 'H':
                countH = countH + 1
            if card[0] == 'S':
                countS = countS + 1

        # No possibility of flush
        if countD < minSuits and countC < minSuits and countH < minSuits and countS < minSuits:
            flushValue = -1

        # Calculate flushValue based on cardValue
        if countD >= minSuits:
            for card in combinedCards:
                if card[0] == 'D':
                    flushValue = flushValue + cardValue(card)
                else:
                    flushValue = flushValue - 1

        elif countC >= minSuits:
            for card in combinedCards:
                if card[0] == 'C':
                    flushValue = flushValue + cardValue(card)
                else:
                    flushValue = flushValue - 1

        elif countH >= minSuits:
            for card in combinedCards:
                if card[0] == 'H':
                    flushValue = flushValue + cardValue(card)
                else:
                    flushValue = flushValue - 1

        elif countS >= minSuits:
            for card in combinedCards:
                if card[0] == 'S':
                    flushValue = flushValue + cardValue(card)
                else:
                    flushValue = flushValue - 1

        # print(flushValue)
        return self.weights[2] * flushValue

    def straightValue(self):

        def cardValue(card):
            if card[1] == 'A':
                value = 14
            elif card[1] == 'K':
                value = 13
            elif card[1] == 'Q':
                value = 12
            elif card[1] == 'J':
                value = 11
            elif card[1] == 'T':
                value = 10
            else:
                value = int(card[1])
            return value

        # Custom comparator to sort cards
        def cardComparator(card1, card2):
            return cardValue(card2) - cardValue(card1)

        straightValue = 1
        straightList = []
        combinedCards = self.community_cards + self.hole_cards
        sortedCards = sorted(combinedCards, cmp=cardComparator)

        # Store card values in list
        for card in sortedCards:
            straightList.append(cardValue(card))

        # Ace can be 14 or 1
        if 14 in straightList:
            straightList.append(1)

        # Count number of consecutive cards
        highCard = straightList[0]
        for idx in range(len(straightList)-1):
            if straightList[idx] == straightList[idx+1] + 1:
                straightValue = straightValue + 1
            else:
                straightValue = straightValue - 1

        return self.weights[3] * straightValue
