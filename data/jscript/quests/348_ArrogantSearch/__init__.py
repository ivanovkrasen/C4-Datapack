# Arrogant Search version 0.1 
# by Fulminus
# in this version, the quest only works as total solo (no option to work with friends) and
# only for the purpose of gaining access to Baium's floor (not for making money via rewards).
print "importing quests:",
import sys
from net.sf.l2j.gameserver.model.quest import State
from net.sf.l2j.gameserver.model.quest import QuestState
from net.sf.l2j.gameserver.model.quest.jython import QuestJython as JQuest
from net.sf.l2j.gameserver.serverpackets import RadarControl
#Quest info
QUEST_NUMBER,QUEST_NAME,QUEST_DESCRIPTION = 348,"ArrogantSearch","An Arrogant Search"

#Messages
default   = "<html><head><body>I have nothing to say to you.</body></html>"
#MOBS TO KILL
ARK_GUARDIAN_ELBEROTH = 5182
ARK_GUARDIAN_SHADOWFANG = 5183
ANGEL_KILLER = 5184
PLATINUM_TRIBE_SHAMAN = 828
PLATINUM_TRIBE_OVERLORD = 829
LESSER_GIANT_MAGE = 657
LESSER_GIANT_ELDER =658

#NPCS TO TALK TO
HANELLIN = 7864
HOLY_ARK_OF_SECRECY_1 = 7977
HOLY_ARK_OF_SECRECY_2 = 7978
HOLY_ARK_OF_SECRECY_3 = 7979
ARK_GUARDIANS_CORPSE = 7980
HARNE = 7144
CLAUDIA_ATHEBALT = 8001
MARTIEN = 7645

#items
TITANS_POWERSTONE = 4287
HANELLINS_FIRST_LETTER = 4288
HANELLINS_SECOND_LETTER = 4289
HANELLINS_THIRD_LETTER = 4290
FIRST_KEY_OF_ARK = 4291
SECOND_KEY_OF_ARK = 4292
THIRD_KEY_OF_ARK = 4293
WHITE_FABRIC_1 = 4294  #to use on Platinum Tribe Shamans/Overlords
BLOODED_FABRIC = 4295
HANELLINS_WHITE_FLOWER = 4394
HANELLINS_RED_FLOWER = 4395
HANELLINS_YELLOW_FLOWER = 4396
BOOK_OF_SAINT = 4397  # Ark2 (after fight with Elberoth)
BLOOD_OF_SAINT = 4398 # Ark1 (after fight with Angel Killer)
BRANCH_OF_SAINT = 4399 # Ark3 (after fight with Shadowfang)
WHITE_FABRIC_0 = 4400  #talk to Hanellin to see what to do (for companions)
WHITE_FABRIC_2 = 5232  #to use on Guardian Angels and Seal Angels

ANTIDOTE = 1831
HEALING_POTION = 1061

#ARK: [key, summon, no-key text, openning-with-key text, already-openned text, content item]
ARKS={
HOLY_ARK_OF_SECRECY_1: [FIRST_KEY_OF_ARK,0,"7977-01.htm","7977-02.htm","7977-03.htm",BLOOD_OF_SAINT],
HOLY_ARK_OF_SECRECY_2: [SECOND_KEY_OF_ARK,ARK_GUARDIAN_ELBEROTH,"That doesn't belong to you.  Don't touch it!","7978-02.htm","7978-03.htm",BOOK_OF_SAINT],
HOLY_ARK_OF_SECRECY_3: [THIRD_KEY_OF_ARK,ARK_GUARDIAN_SHADOWFANG, "Get off my sight, you infidels!","7979-02.htm","7979-03.htm",BRANCH_OF_SAINT],
}

# npc: letter to take, item to check for, 1st time htm, return htm, completed part htm, [x,y,z of chest]
ARK_OWNERS={
HARNE: [HANELLINS_FIRST_LETTER, BLOOD_OF_SAINT, '7144-01.htm', '7144-02.htm', '7144-03.htm', [-418,44174,-3568]],
CLAUDIA_ATHEBALT: [HANELLINS_SECOND_LETTER, BOOK_OF_SAINT, '8001-01.htm', '8001-02.htm', '8001-03.htm', [181472,7158,-2725]],
MARTIEN: [HANELLINS_THIRD_LETTER, BRANCH_OF_SAINT, '7645-01.htm', '7645-02.htm', '7645-03.htm', [50693,158674,376]]
}

#mob: cond, giveItem, amount, chance%, takeItem (assumed to take only 1 of it)
DROPS ={
LESSER_GIANT_MAGE: [2,TITANS_POWERSTONE,1,10,0],
LESSER_GIANT_ELDER: [2,TITANS_POWERSTONE,1,10,0],
ANGEL_KILLER: [5, FIRST_KEY_OF_ARK,1,100,0],
ARK_GUARDIAN_ELBEROTH: [5, SECOND_KEY_OF_ARK,1,100,0],
ARK_GUARDIAN_SHADOWFANG: [5, THIRD_KEY_OF_ARK,1,100,0],
PLATINUM_TRIBE_SHAMAN: [25,BLOODED_FABRIC,1,10,WHITE_FABRIC_1],
PLATINUM_TRIBE_OVERLORD: [25,BLOODED_FABRIC,1,10,WHITE_FABRIC_1],
}

"""
notes:
In order to make it easier to participate in a Baium Raid, the number of Platinum Race monsters that must be
killed to get "Blooded Fabric" in the Arrogant Search quest has been reduced a bit.  However, if a player clicks
"Say that you will come back" to Magister Hanellin while carrying out the quest alone and repeats the quest,
he must hunt the same number of Platinum Race monsters as before.
In the process of delivering the Blooded Fabric to Sir Athebaldt/Iason Heine/Hardin when carrying out the
Arrogant Search quest alone, if it is not the number of "Blooded Fabrics" that the related NPCs want, the
game has been modified to have the player go back to Hanellin. Hanellin gives a reward in proportion to the
number of errands run when the number of "Blooded Fabrics" that have to be delivered is not right and then
the quest is ended.
"""

class Quest (JQuest) :

 def __init__(self,id,name,descr): JQuest.__init__(self,id,name,descr)

 def onEvent (self,event,st) :
    htmltext = event
    if event == "7864_02" :
        st.set("cond","2")
        htmltext = "7864-03.htm"
    elif event == "7864_04a" :  #work alone
        st.set("cond","4")
        st.takeItems(TITANS_POWERSTONE,-1)
        htmltext = "7864-04c.htm"
        st.set("companions","0")
    elif event == "7864_04b" :  #work with friends
        st.set("cond","3")
        st.set("companions","1")
        st.takeItems(TITANS_POWERSTONE,-1)
        htmltext = "not yet implemented"
        #todo: give flowers & handle the multiperson quest...
    return htmltext

 def onTalk (self,npc,st):
    htmltext = default
    id = st.getState()
    npcId = npc.getNpcId()
    cond = st.getInt("cond")
    if npcId == HANELLIN :
        if id == CREATED :
            # if the quest was completed and the player still has a blooded fabric
            # tell them the "secret" that they can use it in order to visit Baium.
            if st.getQuestItemsCount(BLOODED_FABRIC)==1:
                htmltext = "7864-Baium.htm"
                st.exitQuest(1)
            else : #else, start the quest normally
                st.set("cond","0")
                if st.getPlayer().getLevel() < 60 :
                    st.exitQuest(1)
                    htmltext = "7864-01.htm"     #not qualified
                    st.exitQuest(1)
                elif cond==0 :
                    st.setState(PROGRESS)
                    st.set("cond","1")
                    htmltext = "7864-02.htm"    # Successful start: begin the dialog which will set cond=2
        # Player abandoned in the middle of last dialog...repeat the dialog.
        elif cond==1  :
            htmltext = "7864-02.htm"    # begin the dialog which will set cond=2
        # Has returned before getting the powerstone
        elif cond==2 and st.getQuestItemsCount(TITANS_POWERSTONE)==0 :
            htmltext = "7864-03a.htm"    # go get the titan's powerstone
        elif cond==2 :
            htmltext = "7864-04.htm"    # Ask "work alone or in group?"...only alone is implemented in v0.1
        elif cond==4 :
            st.set("cond","5")
            st.giveItems(HANELLINS_FIRST_LETTER,1)
            st.giveItems(HANELLINS_SECOND_LETTER,1)
            st.giveItems(HANELLINS_THIRD_LETTER,1)
            htmltext = "7864-05.htm"    # Go get the 3 sacred relics
        elif cond == 5 and st.getQuestItemsCount(BOOK_OF_SAINT)+st.getQuestItemsCount(BLOOD_OF_SAINT)+st.getQuestItemsCount(BRANCH_OF_SAINT)<3 :
            htmltext = "7864-05.htm"    # Repeat: Go get the 3 sacred relics
        elif cond == 5 :
            htmltext = "7864-06.htm"     # All relics collected!...Get me antidotes & greater healing
            st.takeItems(BOOK_OF_SAINT,-1)
            st.takeItems(BLOOD_OF_SAINT,-1)
            st.takeItems(BRANCH_OF_SAINT,-1)
            st.set("cond","22")
        elif cond == 22 and st.getQuestItemsCount(ANTIDOTE)<5 and st.getQuestItemsCount(HEALING_POTION)<1:
            htmltext = "7864-06a.htm"     # where are my antidotes & greater healing
        elif cond == 22 :
            st.takeItems(ANTIDOTE,5)
            st.takeItems(HEALING_POTION,1)
            if st.getInt("companions") == 0 :
                st.set("cond","25")
                htmltext = "7864-07.htm"    # go get platinum tribe blood...
                st.giveItems(WHITE_FABRIC_1,1)
            else:
                st.set("cond","23")
                htmltext = "not implemented yet"
                st.giveItems(WHITE_FABRIC_0,3)
        elif cond == 25 and st.getQuestItemsCount(BLOODED_FABRIC)<1 :
            htmltext = "7864-07a.htm"
        # the remaining of hanellin's dialogs, including the hunt for Angels which is only done for money,
        # are NOT implemented.
    # Other NPCs follow:
    elif cond == 5:
        if npcId in ARK_OWNERS.keys() :
            # first meeting...have the letter
            if st.getQuestItemsCount(ARK_OWNERS[npcId][0])==1:
                st.takeItems(ARK_OWNERS[npcId][0],1)
                htmltext = ARK_OWNERS[npcId][2]
                st.getPlayer().sendPacket(RadarControl(0,1,ARK_OWNERS[npcId][5][0],ARK_OWNERS[npcId][5][1],ARK_OWNERS[npcId][5][2]))
            # do not have letter and do not have the item
            elif st.getQuestItemsCount(ARK_OWNERS[npcId][1]) < 1:
                htmltext = ARK_OWNERS[npcId][3]
                st.getPlayer().sendPacket(RadarControl(0,1,ARK_OWNERS[npcId][5][0],ARK_OWNERS[npcId][5][1],ARK_OWNERS[npcId][5][2]))
            else:   #have the item (done)
                htmltext = ARK_OWNERS[npcId][4]
        elif npcId in ARKS.keys():
            # if you do not have the key (first meeting)
            if st.getQuestItemsCount(ARKS[npcId][0])==0:
                if ARKS[npcId][1] <> 0 :    # spawn the NPC, if appropriate
                    st.getPcSpawn().addSpawn(ARKS[npcId][1],st.getPlayer().getClientX(),st.getPlayer().getClientY(),st.getPlayer().getClientZ(),120000)
                return ARKS[npcId][2]
            # if the player already has openned the chest and has its content, show "chest empty"
            elif st.getQuestItemsCount(ARKS[npcId][5])==1:  
                htmltext = ARKS[npcId][4]
            else:   # the player has the key and doesn't have the contents, give the contents
                htmltext = ARKS[npcId][3]
                st.takeItems(ARKS[npcId][0],1)
                st.giveItems(ARKS[npcId][5],1)
        elif npcId == ARK_GUARDIANS_CORPSE :
            # if you do not have the key (first meeting)
            if st.getQuestItemsCount(FIRST_KEY_OF_ARK)==0 and st.getInt("angelKillerIsDefeated")==0 :
                st.getPcSpawn().addSpawn(ANGEL_KILLER,st.getPlayer().getClientX(),st.getPlayer().getClientY(),st.getPlayer().getClientZ(),120000)
                htmltext = "7980-01.htm"
            elif st.getQuestItemsCount(FIRST_KEY_OF_ARK)==0 and st.getInt("angelKillerIsDefeated")==1 :
                st.giveItems(FIRST_KEY_OF_ARK,1)
                htmltext = "7980-02.htm"
            else :
                htmltext = "7980-03.htm"
    return htmltext

 def onKill (self,npc,st) :
     npcId = npc.getNpcId()
     if npcId in DROPS.keys() :
         cond = DROPS[npcId][0]
         chance =  DROPS[npcId][3]
         if (st.getInt("cond") == cond) and (st.getQuestItemsCount(DROPS[npcId][1]) < DROPS[npcId][2]) and (st.getRandom(100) < DROPS[npcId][3]) :
             st.giveItems(DROPS[npcId][1],DROPS[npcId][2])
             st.playSound("ItemSound.quest_itemget")
             if DROPS[npcId][4] <> 0:
                 st.takeItems(DROPS[npcId][4],1)
             # in accordance to http://forum.l2jdp.com/viewtopic.php?t=2974
             # quest ends when you get the blooded fabric
             if cond == 25:
                 st.playSound("ItemSound.quest_finish")
                 st.exitQuest(1)
     if npcId == ANGEL_KILLER :
         return "Ha, that was fun! If you wish to find the key, search the corpse"
     return


# Quest class and state definition
QUEST       = Quest(QUEST_NUMBER, str(QUEST_NUMBER)+"_"+QUEST_NAME, QUEST_DESCRIPTION)

CREATED     = State('Start',     QUEST)
PROGRESS    = State('Progress',   QUEST)
COMPLETED   = State('Completed', QUEST)

QUEST.setInitialState(CREATED)
QUEST.addStartNpc(HANELLIN)
CREATED.addTalkId(HANELLIN)
PROGRESS.addTalkId(HANELLIN)
PROGRESS.addTalkId(ARK_GUARDIANS_CORPSE)
for i in ARK_OWNERS.keys() :
    PROGRESS.addTalkId(i)
for i in ARKS.keys() :
    PROGRESS.addTalkId(i)

for i in DROPS.keys():
  PROGRESS.addKillId(i)

print str(QUEST_NUMBER)+": "+QUEST_DESCRIPTION
