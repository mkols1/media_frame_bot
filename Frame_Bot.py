import os
import tweepy
import random
from apscheduler.schedulers.blocking import BlockingScheduler

#started july 7, 2023


f = open('oauth.txt', 'r')
tokens = f.readlines()
api_key = f[0].strip()
api_secret = f[1].strip()
access_token = f[2].strip()
access_token_secret = f[3].strip()
bearer_token = f[4].strip()

client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)

auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

#client.create_tweet(text="test")
#API.media_upload("bananachan.png")


curr_frame = ""
curr_ep = ""

#def pick_image():
#    #Pick a random image from the screenshot folder
#    images = os.listdir('./screenshots')
#    fCount = len(images)
#    return images[random.randint(0,fCount - 1)]
    

#def upload_image():
#    print("\n=======================================================================")
#    fname = pick_image()
#    print("\n" + fname)
#    media = api.media_upload(filename = "./screenshots/" + fname)
#    #print("MEDIA: ", media)
#    try:
#        tweet = client.create_tweet(text = fname, media_ids = [media.media_id])
#        print("\nTWEET: ", tweet)
#    except:
#        upload_image()

def next_frame():
    #gets the filename of the next frame to be uploaded

    global curr_frame
    #all files in current episode to a list
    images = sorted(os.listdir("./Frames/" + curr_ep))

    #get frame # of current frame
    title = curr_frame.replace('.jpg', '')
    #split at " - ", index 2 will contain the numerical number of the episode
    title = title.split(" - ")

    #if at the end of the frames for that episode:
    if int(title[2]) >= len(images):
        #move up to the next episode
        next_ep()
    else:
        #otherwise update the current frame string
        curr_frame = images[int(title[2])]

    return './Frames/' + curr_ep + "/" + curr_frame

def next_ep():
    #move up to the next episode
    global curr_ep
    global curr_frame
    #get list of episode folder names
    folders = sorted(os.listdir("./Frames/"))
    new_ep = curr_ep.split(".")
    new_ep = int(new_ep[0]) #folder # will be index of next
    curr_ep = folders[new_ep]

    #update the curr_frame to the first frame in the new episode
    images = sorted(os.listdir("./Frames/" + curr_ep))
    curr_frame = images[0]

    return


def upload_image():
    print("\n=======================================================================")

    fpath = next_frame()    #get next episode

    print("\n" + fpath)
    media = api.media_upload(filename = fpath)
    tweet = client.create_tweet(text = curr_frame.replace(".jpg", ""), media_ids = [media.media_id])
    print("\nTWEET: ", tweet)
    save_frame()
 

def save_frame():
    #saves last posted frame to file
    #save the name of the current part (folder name)
    #save the name of the last posted frame (file name)
    #both go to a file
    f = open("last_frame.txt", "w")
    f.write(curr_ep + "\n" + curr_frame)
    f.close()
    return

def restore_frame():
    #restore the saved value to curr_frame and curr_ep    
    f = open("last_frame.txt", "r")
    frm = (f.read()).split("\n")
    
    global curr_ep
    global curr_frame 
    curr_ep = frm[0]
    print("Restore curr_ep:" + curr_ep)
    curr_frame = frm[1]
    print("Restore curr_frame:" + curr_frame)
    return

def main():
    up_sched = BlockingScheduler()
    up_sched.add_job(upload_image, 'interval', minutes = 15, start_date = "2023-07-07 09:30:00")
    restore_frame()
    #i=0
    #while i < 5:
    #    upload_image()
    #    #i+=1
    #return
    try:
        up_sched.start()
    except:
        pass

if __name__ == '__main__':
    main()
    #upload_image()
