//Story selection
() => {{
    const getElementByXpath = (Xpath) => {{
        return document.evaluate(Xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    }}
    const set = {set};
    const story = {story};

    const storyBase = '//*[@id="root"]/div/div[4]/div/div/div[2]/div/div[1]/div[Set]/div[story]/div[1]/div[1]/div/img';
    const xpBase = '//*[@id="root"]/div/div[4]/div/div/div[2]/div/div[1]/div[Set]/div[story]/div[2]/div[2]';
    const storyClickBase = '//*[@id="root"]/div/div[4]/div/div/div[2]/div/div[1]/div[Set]/div[story]/div[2]/div/div[1]/a[1]'

    const storyXpath = storyBase.replace('Set', set).replace('story', story);
    const storyClick = storyClickBase.replace('Set', set).replace('story', story);
    const xpXpath = xpBase.replace('Set', set).replace('story', story);
    const xpValue = parseInt(getElementByXpath(xpXpath).textContent);

        getElementByXpath(storyXpath).click();
        getElementByXpath(storyClick).click();
}}





//Match pairs
() => {{
    let tokens = document.querySelectorAll('button[data-test="challenge-tap-token"]');
    for (let i=0; i < tokens.length; i++) {{
        if (tokens[i].classList.contains('pmjld')) {{
            tokens[i].click()
        }}
    }}
    if (!tokens[{first}].disabled && !tokens[{offset}].disabled) {{
        tokens[{first}].click()
        tokens[{offset}].click()
    }}
}}

//Check if continued button is disabled
() => {
    continueButton = document.querySelector('#root > div > div > div > div > div:nth-of-type(3) > div > div > div > button')
    return continueButton.disabled
 }

//Get amount of tokens on screen
() => {
    let tokens = document.querySelectorAll('button[data-test="challenge-tap-token"]');
    if (tokens != null) {
        return tokens.length;
    }
    else {
        return 0;
    } 
}

//Click choices
() => {
    let choices = document.querySelectorAll('button[data-test="stories-choice"]');
    if (choices != undefined && choices.length != 0) {
        for (let i=0; i <= choices.length; i++) {
            try {
                choices[i].click();
            }
            catch (err) {
                break;
            }
        }
    }
}

//Click all tokens
() => {
    let tokens = document.querySelectorAll('button[data-test="challenge-tap-token"]');
    for (let i=0; i <= tokens.length; i++) {
        try {
            tokens[i].click()
        }
        catch (err) {
            break;
        }
    }
}

//Get total XP
() => {
    let sets = document.querySelector('#root > div > div:nth-of-type(4) > div > div > div:nth-of-type(2) > div > div:first-of-type').getElementsByClassName('_2nLk_');
    let set_list = [];
    for (let i=0; i<sets.length; i++) {
        let stories = sets[i].getElementsByClassName('X4jDx');
        let story_list = [];
        for (let i=0; i<stories.length; i++) {
            let story_divs = stories[i].getElementsByTagName('div');
            let story_content = [];
            for (let i=0; i < story_divs.length; i++) {
                let text_content = story_divs[i].innerText;
                if (text_content.includes('XP') && !text_content.includes('\n')) {
                    story_content.push(parseInt(text_content));
                    break;
                }
            }
            story_content.push(stories[i].querySelector('div[data-test="story-title"]').innerText)
            story_list.push(story_content);
        }
        set_list.push(story_list)
    }
    return set_list;
}
