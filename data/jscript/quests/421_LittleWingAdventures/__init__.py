# Upgrade your Hatchling to Strider version 0.2
# by DrLecter & DraX_

#Quest info
QUEST_NUMBER      = 421
QUEST_NAME        = "LittleWingAdventures"
QUEST_DESCRIPTION = "Little Wing's Big Adventures"

#Configuration

#Minimum pet and player levels required to complete the quest (defaults 55 and 45)
MIN_PET_LEVEL = 55
MIN_PLAYER_LEVEL = 45
# Maximum distance allowed between pet and owner; if it's reached while talking to any NPC, quest is aborted
MAX_DISTANCE = 100

#Messages
default = "<html><head><body>I have nothing to say to you.</body></html>"
event_1 = "<html><head><body>Sage Cronos:<br>Then go and see <font color=\"LEVEL\">Fairy Mymyu</font>, she will help you</body></html>"
error_1 = "<html><head><body>You're suppossed to own a hatchling and have it summoned to complete this quest.</body></html>"
error_2 = "<html><head><body>Hey! What happened with the other hatchling you had? This one is different.</body></html>"
error_3 = "<html><head><body>Sage Cronos:<br>You need to be level "+str(MIN_PLAYER_LEVEL)+" to complete this quest.</body></html>"
error_4 = "<html><head><body>Sage Cronos:<br>Your pet need to be level "+str(MIN_PET_LEVEL)+" to complete this quest.</body></html>"
error_5 = "Your pet is not a hatchling. Quest Aborted."
error_6 = "Your pet should be nearby. Quest aborted"
qston_1 = "<html><head><body>Sage Cronos:<br>So, you want to turn your hatchling into a more powerful creature?<br><br><a action=\"bypass -h Quest "+str(QUEST_NUMBER)+"_"+QUEST_NAME+" 16\">Yes, please tell me how</a><br></body></html>"
qston_2 = "<html><head><body>Sage Cronos:<br>I've said you need to talk to <font color=\"LEVEL\">Fairy Mymyu</font>!!!. Am i clear???</body></html>"
qston_3 = "<html><head><body>Fairy Mymyu:<br>You weren't yet able to find the <font color=\"LEVEL\">Fairy Trees of Wind, Star, Twilight and Abyss</font>? Don't give up! They are all in <font color=\"LEVEL\">Hunter's Valley</font></body></html>"
order_1 = "<html><head><body>Fairy Mymyu:<br>Your pet must drink the sap of <font color=\"LEVEL\">Fairy Trees of Wind, Star, Twilight and Abyss</font> to grow up. The trees will probably agree but as we don't want to hurt them, take that leafs to heal any wound your hatchling could cause them</body></html>"
ftm_11  = "<html><head><body>Fairy Tree of Wind: <br>I'll let your hatchling drink from my sap, but you will have to cover the wound your pet will do on me with one of these leafs you have, they are hypoallergenic<br><br><a action=\"bypass -h Quest "+str(QUEST_NUMBER)+"_"+QUEST_NAME+" 1\">It's ok</a></body></html>"
ftm_12  = "The hatchling has drunk the sap of the fairy tree of the wind."
ftm_21  = "<html><head><body>Fairy Tree of Star: <br>Oh! One of those nasty ghosts hurted my bark... look! Only a fairy leaf could cure my wound... <br><br><a action=\"bypass -h Quest "+str(QUEST_NUMBER)+"_"+QUEST_NAME+" 2\">Give it a leaf</a></body></html>"
ftm_22  = "The hatchling has drunk the sap of the fairy tree of the star."
ftm_31  = "<html><head><body>Fairy Tree of Twilight: <br>Ok, i do know the way this is supposed to be, but we don't have the time to wait your hacthling to hit me for hours... Let's make it quick<br><br><a action=\"bypass -h Quest "+str(QUEST_NUMBER)+"_"+QUEST_NAME+" 4\">Fine, take the leaf</a></body></html>"
ftm_32  = "The hatchling has drunk the sap of the fairy tree of the twilight."
ftm_41  = "<html><head><body>Fairy Tree of Abyss: <br>That your pet will bite me and you gonna put a leaf in my wound? No way! No! Wait!... argh... if i could run like Black Willows do...<br><br><a action=\"bypass -h Quest "+str(QUEST_NUMBER)+"_"+QUEST_NAME+" 8\">Say sorry</a></body></html>"
ftm_42  = "The hatchling has drunk the sap of the fairy tree of the abyss."
end_msg = "<html><head><body>Fairy Mymyu:<br>Great job, your hatchling"
end_msg2= "has become an strider, enjoy!</body></html>"

#Quest items
FT_LEAF = 4325
CONTROL_ITEMS = { 3500:4422, 3501:4423, 3502:4424 }

#NPCs
SG_CRONOS = 7610
FY_MYMYU  = 7747
#NpcId, bitmask, spawnX,spawnY,spawnZ,msg1,msg2
FAIRY_TREES = [ [5185,1,128091,90400,-1998,ftm_11,ftm_12],
                [5186,2,117935,94080,-2096,ftm_21,ftm_22],
                [5187,4,113449,93928,-2072,ftm_31,ftm_32],
                [5188,8,106685,92608,-2162,ftm_41,ftm_42] ]
#Mobs
GUARDIAN = 5189

import sys
from net.sf.l2j.gameserver.model.quest import State
from net.sf.l2j.gameserver.model.quest import QuestState
from net.sf.l2j.gameserver.model.quest.jython import QuestJython as JQuest

def get_control_item(st) :
  item = st.getPlayer().getPet().getControlItemId()
  if st.getState() == CREATED :
      st.set("item",str(item))
  else :
      if  int(st.get("item")) != item : item = 0
  return item  

def get_distance(st) :
    is_far = False
    if abs(st.getPlayer().getPet().getX() - st.getPlayer().getX()) > MAX_DISTANCE :
        is_far = True
    if abs(st.getPlayer().getPet().getY() - st.getPlayer().getY()) > MAX_DISTANCE :
        is_far = True
    if abs(st.getPlayer().getPet().getZ() - st.getPlayer().getZ()) > MAX_DISTANCE :
        is_far = True
    return is_far

class Quest (JQuest) :

 def __init__(self,id,name,descr): JQuest.__init__(self,id,name,descr)

 def onEvent (self,event,st) :
    htmltext = event
    leafs = st.getQuestItemsCount(FT_LEAF) 
    for i in range(4) :
       if event == str(FAIRY_TREES[i][1]) :
           st.set("id", str(int(st.get("id")) | FAIRY_TREES[i][1]))
           htmltext = FAIRY_TREES[i][6]
           st.takeItems(FT_LEAF,1)
           if 1 < leafs <= 4 :
              st.playSound("ItemSound.quest_itemget")
           elif leafs == 1 and int(st.get("id")) == 15:
              st.playSound("ItemSound.quest_middle")
              st.set("cond","3")
              st.setState(STARTED)
    if event == "16" :
       htmltext = event_1
       st.setState(STARTING)
       st.set("id","0")
       st.set("cond","1")
       st.playSound("ItemSound.quest_accept")
    return htmltext

 def onTalk (self,npc,st):
   htmltext = default
   id = st.getState()
   npcid = npc.getNpcId()
   if st.getPlayer().getPet() == None :
       htmltext = error_1
       st.exitQuest(1)
   elif st.getPlayer().getPet().getTemplate().npcId not in [12311,12312,12313] : #npcids for hatchlings
       htmltext = error_5
       st.exitQuest(1)
   elif st.getPlayer().getPet().getLevel() < MIN_PET_LEVEL :
       st.exitQuest(1)
       htmltext = error_4
   elif get_distance(st) :
       st.exitQuest(1)
       htmltext = error_6
   elif get_control_item(st) == 0 :
       st.exitQuest(1)
       htmltext = error_2
   elif npcid == SG_CRONOS :
      if id == CREATED :
         if st.getPlayer().getLevel() < MIN_PLAYER_LEVEL :
            st.exitQuest(1)
            htmltext = error_3
         else :   
            htmltext = qston_1
      else :
         htmltext = qston_2
   elif npcid == FY_MYMYU :
     if id == STARTING :
        if st.getQuestItemsCount(FT_LEAF) == 0 and int(st.get("id")) == 0 :
           st.set("cond","2")
           st.giveItems(FT_LEAF,4)
           st.playSound("ItemSound.quest_itemget")
           htmltext = order_1
        else :
            htmltext = qston_3
     elif id == STARTED :
        st.setState(COMPLETED)
        st.exitQuest(1)
        st.playSound("ItemSound.quest_finish")
        name = st.getPlayer().getPet().getName()
        if name == None : name = " "
        else : name = " "+name+" "
        htmltext = end_msg+name+end_msg2
        item=CONTROL_ITEMS[st.getPlayer().getInventory().getItemByObjectId(st.getPlayer().getPet().getControlItemId()).getItemId()]
        st.getPlayer().getPet().deleteMe(st.getPlayer()) #both despawn pet and delete controlitem
        st.giveItems(item,1)
   else:
     leafs = st.getQuestItemsCount(FT_LEAF)
     if 0 < leafs :
        for i in range(4) :
           if npcid == FAIRY_TREES[i][0] and (int(st.get("id")) | FAIRY_TREES[i][1] != int(st.get("id"))) :
              for j in range(2):
                 for k in range(2): 
                    st.getPcSpawn().addSpawn(GUARDIAN,FAIRY_TREES[i][2]+70*pow(-1,j%2),FAIRY_TREES[i][3]+70*pow(-1,k%2),FAIRY_TREES[i][4])
              htmltext = FAIRY_TREES[i][5]
   return htmltext

 def onKill (self,npc,st) :
   return  

# Quest class and state definition
QUEST       = Quest(QUEST_NUMBER, str(QUEST_NUMBER)+"_"+QUEST_NAME, QUEST_DESCRIPTION)
CREATED     = State('Start',     QUEST)
STARTING    = State('Starting',  QUEST)
STARTED     = State('Started',   QUEST)
COMPLETED   = State('Completed', QUEST)

QUEST.setInitialState(CREATED)

# Quest NPC starter initialization
QUEST.addStartNpc(SG_CRONOS)
# Quest initialization
CREATED.addTalkId(SG_CRONOS)

STARTING.addTalkId(SG_CRONOS)
STARTING.addTalkId(FY_MYMYU)

STARTED.addTalkId(FY_MYMYU)

STARTING.addQuestDrop(SG_CRONOS,FT_LEAF,1)

for i in range(4) :
  STARTING.addTalkId(FAIRY_TREES[i][0])

print "importing quests: "+str(QUEST_NUMBER)+": "+QUEST_DESCRIPTION
