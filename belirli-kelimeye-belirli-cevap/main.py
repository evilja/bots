import praw
import random
import evilparser


client_id     = ""
client_secret = ""
username      = ""
password      = ""
user_agent    = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
reddit = praw.Reddit(client_id = client_id,
                     client_secret = client_secret,
                     username = username,
                     password = password,
                     user_agent = user_agent)



subreddit = reddit.subreddit("herseycokguzelolacak")

x = evilparser.parser()
config = x.getconf("evilconf",verbose=True)
def randomtextsec():
    return config["textler"][random.randint(0,len(config["textler"])-1)]
while True:

    for comnt in subreddit.stream.comments(skip_existing=True):

        if comnt.author.name.lower() in config["sikilmesi_gereken_hesaplar"]:

            if "".join(config["tetikleyici"].split(" ")).lower().replace(",","").replace(".","") in "".join(comnt.body.lower().split(" ")).replace(".","").replace(",",""):
                asd = randomtextsec()
                print(comnt.author.name+" -- "+asd[0:25])
                comnt.reply(body=f"{asd}. ({config['tetikleyici']})\n\n^(Bu bir bot. {comnt.author.name} adlı şahısın annesini sikmek için geliştirildi)")
