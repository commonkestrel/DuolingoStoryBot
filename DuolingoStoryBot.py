from pyppeteer import launch
import json
import asyncio
import time

duoUrl = 'https://www.duolingo.com'

def getLogin():
    loginPath = 'Assets/login.json'
    try:
        loginFile = open(loginPath, 'r')
        login = loginFile.readlines()[0]
        login = json.loads(login)
        
    except FileNotFoundError:
        loginFile = open(loginPath, 'w')
        
        login = {}
        login['user'] = input('Duolingo Username: ')
        login['pass'] = input('Duolingo Password: ')

        rememberInput = input('Remember login? (y/n): ')
        if rememberInput.lower() == 'y':
            remember = True
        elif rememberInput.lower() == 'n':
            remember = False
        else:
            remember = None
        while remember == None:
            rememberInput = input('Invalid input. Remember login? (y/n): ')
            if rememberInput.lower() == 'y':
                remember = True
            elif rememberInput.lower() == 'n':
                remember = False
            else:
                remember = None
        
        if remember:
            loginJson = json.dumps(login)
            loginFile.write(loginJson)
        
        loginFile.close()
        
    return login['user'], login['pass']
        
async def login():
    userSelector = 'input[data-test="email-input"]'
    passSelector = 'input[data-test="password-input"]'
    duoSubmit = 'button[data-test="register-button"]'
    loginSelector = '#root > div > div > span:nth-child(2) > div > div._18cH1 > div._3wkBv > div._3uMJF > button'
    
    await page.click(loginSelector)
    await page.waitForSelector(userSelector)

    duoUser, duoPass = getLogin()
    
    await page.type(userSelector, duoUser)
    await page.type(passSelector, duoPass)
    
    await page.click(duoSubmit)
    await page.waitForSelector('div[data-test="skill"]')
    
async def storySelect(maxXp):
    with open('Assets/scripts.js') as script:
        selectBase = ''.join(script.readlines()[1:24])
    await page.goto(duoUrl + '/stories'),

    earnedXp = 0
    for Set in range(2, 71, 1):
        for Story in range(2, 6, 1):
            firstXpath = '//*[@id="root"]/div/div[4]/div/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/img'
            await page.waitForXPath(firstXpath)
            selectScript = selectBase.format(set=Set, story=Story)
            click = await page.evaluate(selectScript)
            
            if click == 0:
                continue
            
            await storyComplete()
            earnedXp += click
            if maxXp != 0 and earnedXp >= maxXp:
                print(f'Successfully earned {earnedXp}')
                return
            
async def waitForEnabled(selector, timeout=30):
    await page.waitForSelector(selector)
    disabled = True
    startTime = time.time()
    while disabled:
        disabled = await page.evaluate(f'''() => {{
            finalButton = document.querySelector('{selector}');
            return finalButton.disabled
            }}''')
        if disabled:
            if time.time() - startTime > timeout:
                return 1
    return 0
            
async def match():
    global scripts
    for offset in range(5):
        for i in range(5):
            individualOffset = 5 + ((i + offset) % 5)
            matchScript = ''.join(scripts[26:38]).format(offset=individualOffset, first=i)
            await page.evaluate(matchScript)
        time.sleep(1)
        
            
async def storyComplete():
    global scripts
    continueSelector = '#root > div > div > div > div > div:nth-of-type(3) > div > div > div > button'
    writeExersize = 'Buenos diás, buenos diás, buenos diás, buenos diás, buenos diás, buenos diás, buenos diás.'
    finalSelector = 'button[data-test="stories-player-done"]'
    altFinal = 'button[data-test="stories-player-continue"]'
    textSelector = 'textarea[placeholder="Type your response in Spanish!"]'
    await page.waitForSelector(continueSelector)
    
    while True:
        try:
            disabledScript = ''.join(scripts[40:44])
            disabled = await page.evaluate(disabledScript)
            if disabled != 'true':
                await page.click(continueSelector)
        except:
            break
        else:
            choiceScript = ''.join(scripts[57:70])
            await page.evaluate(choiceScript)
            
            lengthScript = ''.join(scripts[46:55])
            tokensLength = await page.evaluate(lengthScript)
            
            if tokensLength == 10:
                matched = 1
                while matched == 1:
                    await match()
                    matched = await waitForEnabled(continueSelector, timeout=3)
                await page.click(continueSelector)
                
                try:
                    await waitForEnabled(continueSelector, timeout=4)
                    await page.click(continueSelector)
                    await page.waitForSelector(textSelector, {'timeout': 4000}) #Check if there is a write excersize
                    await page.type(textSelector, writeExersize)
                except: #Exit main loop if no write excersize
                    break

            elif tokensLength != 0:
                tokenScript = ''.join(scripts[72:83])
                await page.evaluate(tokenScript)
            
    try:
        await page.waitForSelector(finalSelector, {'timeout': 4000})
        await waitForEnabled(finalSelector)
        await page.click(finalSelector)
    except:
        await page.waitForSelector(altFinal, {'timeout': 4000})
        await waitForEnabled(altFinal)
        await page.click(altFinal)
    try:
        await page.waitForXPath('//*[@id="root"]/div/div[4]/div/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/img', {'timeout': 10000})
    except:
        await page.waitForSelector(finalSelector, {'timeout': 4000})
        await waitForEnabled(finalSelector)
        await page.click(finalSelector)
      
async def main():
    global browser
    global page
    
    #Get headless mode and check if it is valid
    headlessInput = input('Run in background? (y/n): ')
    if headlessInput.lower() == 'y':
        headless = True
    elif headlessInput.lower() == 'n':
        headless = False
    else:
        headless = None
    while headless == None:
        headlessInput = input('Invalid input. Run in background? (y/n): ')
        if headlessInput.lower() == 'y':
            headless = True
        elif headlessInput.lower() == 'n':
            headless = False
        else:
            headless = None

    #Get maximum xp to earn and check if it is an integer
    inputMaxXp = input("Xp amount to terminate after: ")
    try:
        maxXp = int(inputMaxXp)
        maxSuccess = True
    except:
        maxSuccess = False
    while not maxSuccess:
        inputMaxXp = input("Must be an integer. Xp amount to terminate after: ")
        try:
            maxXp = int(inputMaxXp)
            maxSuccess = True
        except:
            maxSuccess = False
    
    #Open browser and go to duolingo.com
    browser = await launch(headless=headless, args=['--mute-audio'])
    page = await browser.newPage()
    await page.goto(duoUrl)

    global scripts
    with open('Assets/scripts.js', 'r') as f:
        scripts = f.readlines()
    
    await login() #Login with provided credientials
    await storySelect(maxXp)
    
    await browser.close()#Close browser when done
    
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
