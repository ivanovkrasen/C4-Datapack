# Made by Fulminus
# Quest 347: Go Get The Calculator.

import sys
from net.sf.l2j.gameserver.model.quest import State
from net.sf.l2j.gameserver.model.quest import QuestState
from net.sf.l2j.gameserver.model.quest.jython import QuestJython as JQuest

# NPCs to talk to
BRUNON = 7526
SILVERA = 7527
SPIRON = 7532
BALANKI = 7533

# MOBs to kill
GEMSTONE_BEAST = 540    # drops "gemstone beast's crystal" at 50% chance

# quest items
GEMSTONE_BEAST_CRYSTAL = 4286
ADENA = 57
CALCULATOR_Q = 4285
CALCULATOR = 4393

class Quest (JQuest) :

 def __init__(self,id,name,descr): JQuest.__init__(self,id,name,descr)

 def onEvent (self,event,st) :
    htmltext = event
    if event == "1" :
        st.set("id","0")
        st.set("cond","1")
        st.setState(STARTED)
        st.playSound("ItemSound.quest_accept")
        htmltext = str(BRUNON)+"-02.htm"
    elif event == "7533_1" :
        if st.getQuestItemsCount(ADENA)>100 :
            st.takeItems(ADENA, 100)
            if int(st.get("cond"))== 1:
                st.set("cond","2")
            else :
                st.set("cond","4")
            htmltext = str(BALANKI)+"-02.htm"
        else :
            htmltext = str(BALANKI)+"-03.htm"
    elif event == "7532_1" :
        htmltext = str(SPIRON)+"-02a.htm"
        if int(st.get("cond"))== 1:
            st.set("cond","3")
        else :
            st.set("cond","4")
    elif event == "7532_2" :
        htmltext = str(SPIRON)+"-02b.htm"
    elif event == "7532_3" :
        htmltext = str(SPIRON)+"-02c.htm"
    elif event == "7526_1" :
        st.giveItems(CALCULATOR,1)
        st.takeItems(CALCULATOR_Q,1)
        st.playSound("ItemSound.quest_middle")
        st.setState(COMPLETED)
        st.set("cond","0")
        st.exitQuest(1)
        htmltext = str(BRUNON)+"-05.htm"
    elif event == "7526_2" :
        st.giveItems(ADENA,1000)
        st.takeItems(CALCULATOR_Q,1)
        st.playSound("ItemSound.quest_middle")
        st.setState(COMPLETED)
        st.set("cond","0")
        st.exitQuest(1)
        htmltext = str(BRUNON)+"-06.htm"
    return htmltext


 def onTalk (Self,npc,st):

    npcId = npc.getNpcId()
    htmltext = "<html><head><body>I have nothing to say you</body></html>"
    id = st.getState()
    if npcId == BRUNON and id==CREATED :
        st.set("id","0")
        st.set("cond","0")
        htmltext = str(BRUNON)+"-01.htm"
    elif npcId == BRUNON and int(st.get("cond"))>0 and st.getQuestItemsCount(CALCULATOR_Q)==0 :
        htmltext = str(BRUNON)+"-03.htm"
    elif npcId == BALANKI and (int(st.get("cond"))==1 or int(st.get("cond"))==3):
        htmltext = str(BALANKI)+"-01.htm"
    elif npcId == SPIRON and (int(st.get("cond"))==1 or int(st.get("cond"))==2) :
        htmltext = str(SPIRON)+"-01.htm"
    elif npcId == SILVERA and int(st.get("cond"))==4 :
        st.set("cond","5")
        htmltext = str(SILVERA)+"-01.htm"
    elif npcId == SILVERA and int(st.get("cond"))==5 and st.getQuestItemsCount(GEMSTONE_BEAST_CRYSTAL)<10 :
        htmltext = str(SILVERA)+"-02.htm"
    elif npcId == SILVERA and int(st.get("cond"))==5 and st.getQuestItemsCount(GEMSTONE_BEAST_CRYSTAL)==10 :
        htmltext = str(SILVERA)+"-03.htm"
        st.takeItems(GEMSTONE_BEAST_CRYSTAL,10)
        st.giveItems(CALCULATOR_Q,1)
        st.playSound("ItemSound.quest_itemget")
        st.set("cond","6")
    elif npcId == BRUNON and int(st.get("cond"))==6 and st.getQuestItemsCount(CALCULATOR_Q)==1 :
        htmltext = str(BRUNON)+"-04.htm"
    return htmltext

 def onKill (self,npc,st):

   npcId = npc.getNpcId()
   if npcId == GEMSTONE_BEAST and int(st.get("cond"))==5 and st.getRandom(2)==1 and st.getQuestItemsCount(GEMSTONE_BEAST_CRYSTAL)<10 :
        st.giveItems(GEMSTONE_BEAST_CRYSTAL,1)
        if st.getQuestItemsCount(GEMSTONE_BEAST_CRYSTAL) == 10 :
            st.playSound("ItemSound.quest_middle")
        else:
            st.playSound("ItemSound.quest_itemget")
   return

QUEST       = Quest(347,"347_GoGetTheCalculator","Calculator")
CREATED     = State('Start', QUEST)
STARTED     = State('Started', QUEST)
COMPLETED   = State('Completed', QUEST)


QUEST.setInitialState(CREATED)
QUEST.addStartNpc(BRUNON)

CREATED.addTalkId(BRUNON)

STARTED.addTalkId(BRUNON)
STARTED.addTalkId(SILVERA)
STARTED.addTalkId(SPIRON)
STARTED.addTalkId(BALANKI)

STARTED.addKillId(GEMSTONE_BEAST)
STARTED.addQuestDrop(GEMSTONE_BEAST, GEMSTONE_BEAST_CRYSTAL, 1)

print "importing quests: 347: Go Get The Calculator"
