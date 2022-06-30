import re
import text_tools
from dataclasses import dataclass
import random
# find "XdY +/- Z"
dice_regex = re.compile("\\b((?:[1-9][0-9]*)?d[1-9][0-9]*)\s*([+-]\s*[0-9]+)?\\b")

# find whitespace and a plus to remove
plus_whitespace_regex = re.compile("\\s+|\+")

# find "adv" or "dis"
adv_dis_regex = re.compile("\\b(adv|dis)")

@dataclass
class DiceResult:
    numDice: int
    numSides: int
    mod: int
    resultList: list
    adv: int

    def getRollName(self) -> str:
        msg = str(self.numDice) + 'd' + str(self.numSides)
        if self.mod > 0:
           msg += "+" + str(self.mod) 
        elif self.mod < 0:
            msg += "-" + str(self.mod) 

        if self.adv == 1:
            msg += " with adv"
        elif self.adv == -1:
            msg += " with dis"


        return msg

    def getResults(self) -> str:
        msg = ""
        if self.adv == 0:
            for res in self.resultList:

                msg += str(res)
                if self.numSides == 20:
        
                    if res == 20:
                        msg += + " *CRIT*"
                    elif res == 1:
                        msg += " *CRIT FAIL*\n"
            
                msg += '\n' 

            if self.mod > 0:    
                modifier_msg = "Modifer: " + str(self.mod) + '\n'
                

                val = sum(self.resultList) + self.mod

                modifier_msg  += "Result: " + str(val) + '\n'

                msg += text_tools.add_bar(modifier_msg, "above")

        elif self.adv == 1:
            for res in self.resultList:
       
                msg += str(res)
                if self.numSides == 20:
        
                    if res == 20:
                        msg += + " *CRIT*"
                    elif res == 1:
                        msg += " *CRIT FAIL*\n"
            
                msg += '\n' 

            if self.mod > 0:    
                modifier_msg = "Modifer: " + str(self.mod) + '\n'
                

                val = sum(self.resultList) + self.mod

                modifier_msg  += "Result: " + str(val) + '\n'

                msg += text_tools.add_bar(modifier_msg, "above")


        return msg

def _getMod(msg:str) -> int:
    mod = re.sub(plus_whitespace_regex, '', msg)
    print(mod)
    return int(mod)

def _getAdv(msg:str) -> int:
    adv = 0

    results = adv_dis_regex.findall(msg)
    print(results)

    if results:
        if results[0] == "adv":
            adv = 1
        elif results[0] == "dis":
            adv = -1
        else:
            raise Exception(f"Unknown advantage type {results[0]}")
    return adv

def roll(msg:str):
    results = dice_regex.findall(msg)
    adv = _getAdv(msg)

    print(results)

    response = ""

    dice_list = []

    for res in results:
        dice_num, dice_sides = res[0].split('d')
        if dice_num == "":
            dice_num = 1
        if res[1]:
            mod = _getMod(res[1])
        else:
            mod = 0
        dice_num = int(dice_num)
        dice_sides = int(dice_sides)

        # roll the dice. roll twice for each if rolling with adv or dis
        if adv == 0:
            result_list = [random.randint(1, dice_sides) for die in range(dice_num)]
        else:
            result_list = [(random.randint(1, dice_sides), random.randint(1, dice_sides)) for die in range(dice_num)]

        diceRoll = DiceResult(numDice=dice_num, numSides=dice_sides, mod=mod, resultList=result_list, adv=adv)

        dice_list.append(diceRoll)

        if dice_num > 100:
            raise Exception("Please roll less than 100 dice")

        print("HERE")

    if dice_list:
        response = "Rolling "

        if len(dice_list) == 1:
            response += dice_list[0].getRollName()

        elif len(dice_list) == 2:
            response += dice_list[0].getRollName() +  " and " + dice_list[1].getRollName()

        else:
            for ii in range(len(dice_list)):
                if ii == len(dice_list) - 1:
                    response += "and " + dice_list[ii].getRollName()
                else:
                    response += dice_list[ii].getRollName() + ", "

        response = text_tools.add_bar(response, "below")

        if len(dice_list) > 1:
            for dice in dice_list:
                dice_name = dice.getRollName()
                response += text_tools.add_bar(dice_name, "below")

                response += dice.getResults()
        else:
            response += dice_list[0].getResults()

    else:
        raise Exception("Invalid message format. Please write NdN for dice rolls.")

    return response