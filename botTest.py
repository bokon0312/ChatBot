import telegram;
import sys
from io import BytesIO
from time import sleep;
from transitions import State
from transitions.extensions import GraphMachine as Machine
import pygraphviz
class TocMachine(Machine):
	pass

machine = TocMachine(
    states=[
        'user',
        'Japanese',
        'pure music',
		'Jpop',
		'Game',
		'Jazz-hiphop',
		'symphony'
    ],
    transitions=[
        {
            'trigger': 'go_Japanese',
            'source': 'user',
            'dest': 'Japanese',
        },
		{
            'trigger': 'go_pure music',
            'source': 'user',
            'dest': 'pure music',
        },
        {
            'trigger': 'go_Jpop',
            'source': 'Japanese',
            'dest': 'Jpop',
        },
		{
            'trigger': 'go_Game',
            'source': 'Japanese',
            'dest': 'Game',
        },
		{
            'trigger': 'go_Jazz-hiphop',
            'source': 'pure music',
            'dest': 'Jazz-hiphop',
        },
		{
            'trigger': 'go_symphony',
            'source': 'pure music',
            'dest': 'symphony',
        },
        {
            'trigger': 'go_back',
            'source': [
                'Japanese',
        		'pure music',
				'Jpop',
				'Game',
				'Jazz-hiphop',
				'symphony'
            ],
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True
)
machine.get_graph().draw('state_diagram.png',prog='dot')

BOT_TOKEN="505762054:AAG3v48BF8d-V9RO2W2yhERaNAn0TkXEq1g";
Bot=telegram.Bot(BOT_TOKEN);
lastMessageId=0;
def switchstate(user_id,com):
	flag=False;
	if(com=='back'or com=='symphony'or com=='Jazz-hiphop'or com=='Game'or com=='Jpop'or com=='pure music'or com=='Japanese'):
		print("success");
		machine.trigger("go_"+com);
	else:
		text2="I don't understand what you say.";
		flag=True;
	print("I am in "+machine.state+" now");
	if(machine.state=='Japanese'and flag==False):
		text2="Which do you prefer,Jpop or Game ?";
		flag=True;
	elif(machine.state=='pure music'and flag==False):
		text2="Which do you prefer,Jazz_hiphop or symphony ?";
		flag=True;
	elif(machine.state=='Jpop'and flag==False):
		text2="I recommend you https://www.youtube.com/watch?v=U7EBCFQzAQo,type back to exit";
		flag=True;
	elif(machine.state=='Game'and  flag==False):
		text2="I recommend you https://www.youtube.com/watch?v=ZOwf8nz5dN4,type back to exit";
		flag=True;
	elif(machine.state=='Jazz-hiphop'and flag==False):
		text2="I recommend you https://www.youtube.com/watch?v=AULG4MoYxQk,type back to exit";
		flag=True;
	elif(machine.state=='symphony'and flag==False):
		text2="I recommend you https://www.youtube.com/watch?v=kZi5JmD9Bhg,type back to exit";
		flag=True;
	elif(machine.state=='user'):
		text2="For the begining,which do you prefer,Japanese or pure music ?";
		flag=True;
	if(flag):
		Bot.sendMessage(user_id,text2);
		flag=False;
	print("I am in "+machine.state);
	return;

def getText(Update):
	return Update["message"]["text"];

def getMessageId(Update):
	return Update["update_id"];

def messageHandler(Update):
	global lastMessageId;
	flag=False;
	text=getText(Update);
	msg_id=getMessageId(Update);
	user_id=getUserId(Update);
	lastMessageId=msg_id;
	Bot.sendMessage(user_id,text);
	print(user_id,msg_id,text);
	print(text);
	switchstate(user_id,text);
	return;

def getChatId(Update):
	return Update["message"]["chat"]["id"];
def getUserId(Update):
	return Update["message"]["from_user"]["id"];

def main():
	global lastMessageId;
	Updates=Bot.getUpdates();
	if(len(Updates)>0):
		lastMessageId=Updates[-1]["update_id"];
	while(True):
		Updates=Bot.getUpdates(offset=lastMessageId,timeout = 1);
		Updates=[Update for Update in Updates if Update["update_id"]>lastMessageId]
		for Update in Updates:
			messageHandler(Update);
		sleep(0.5);




if __name__=="__main__":
	main();
