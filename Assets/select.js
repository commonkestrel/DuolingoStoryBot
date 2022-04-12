() => {
    const getElementByXpath = (Xpath) => {
        return document.evaluate(Xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    }
    const set = replace;
    const story = replace;

    const storyBase = '//*[@id="root"]/div/div[4]/div/div/div[2]/div/div[1]/div[Set]/div[story]/div[1]/div[1]/div/img';
    const xpBase = '//*[@id="root"]/div/div[4]/div/div/div[2]/div/div[1]/div[Set]/div[story]/div[2]/div[2]';
    const storyClickBase = '//*[@id="root"]/div/div[4]/div/div/div[2]/div/div[1]/div[Set]/div[story]/div[2]/div/div[1]/a[1]'

    const storyXpath = storyBase.replace('Set', set).replace('story', story);
    const storyClick = storyClickBase.replace('Set', set).replace('story', story);
    const xpXpath = xpBase.replace('Set', set).replace('story', story);
    const xpValue = parseInt(getElementByXpath(xpXpath).textContent);

    if (xpValue > 0) {
        getElementByXpath(storyXpath).click();
        getElementByXpath(storyClick).click();
        return xpValue
    }
    else {return xpValue}
}
