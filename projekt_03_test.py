from playwright.sync_api import Page, sync_playwright
import pytest

@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo =1000)     #spustí prohlížeč
        page = browser.new_page()
        page.goto("https://www.lidl.cz/")
        yield page

 #testovani názvu stránky
def test_title(page: Page):                 
    assert page.title() == "Lidl, správná volba - v prodejnách i online"    #porovnání jestli název odpovídá


#testování cookies
def test_cookies(page: Page):                
    button = page.locator("#onetrust-reject-all-handler").click()       #identifikuji tlačítko Odmitnout                          
    assert page.locator("#onetrust-button-group-parent").is_visible() == False        #zjistím jestli se okno s cookies zavřelo

 #testování neplatného přihlášení
def test_loggin (page: Page):              
    button_cookies = page.locator("#onetrust-reject-all-handler").click()       #odkliknu cookies
    
    page.locator("#__nuxt > div:nth-child(2) > div > div.n-header__root.one-cx > div.n-navigation > div.n-navigation__top-menu-hook > div > div.n-navigation__top-menu-wrapper > nav > ol > li:nth-child(8) > a > span > span").click()
    page.locator("#layout-container > div.layout-container__wrapper--with-header.w-full.relative.flex.flex-col.flex-1.items-center.justify-betweenundefined > div > section > div.email-phone-slide-container > div > div.input-text.w-full.flex.flex-col.space-y-\[4px\].email-animation > div > div > label > input").fill("abc@cba")
    page.locator("#layout-container > div.layout-container__wrapper--with-header.w-full.relative.flex.flex-col.flex-1.items-center.justify-betweenundefined > div > section > div.input-text.w-full.flex.flex-col.space-y-\[4px\] > div > div > label > input").fill("1111")
    page.locator("#duple-button-block > button > span").click()

    error_mesage = page.locator("#layout-container > div.layout-container__wrapper--with-header.w-full.relative.flex.flex-col.flex-1.items-center.justify-betweenundefined > div > section > div.email-phone-slide-container > div > div.input-text.w-full.flex.flex-col.space-y-\[4px\].email-animation > div.w-full.flex.items-start.space-y-\[4px\].pt-1.pb-1.pl-3.pr-3.bg-red-50.rounded > p")
    assert error_mesage.is_visible()


#funkce na zjištení jestli stránka funguje a umí přidat položku do košíku. Ověření, jestli při zvolení "Pokračovat bez registrace" se ukážou chybové hlášky že pole jsou povinná.
def test_add_to_cart (page: Page):

#odkliknu cookies
    button_cookies = page.locator("#onetrust-reject-all-handler")
    button_cookies.click()       

# vložení inputu "froté ručník" a následné zmáčknutí "Entru"  
    input= page.locator("#s-search-input-field")
    input.fill("froté ručník")

    button_search = page.locator("#search-input-hook > div.s-cx-search-input-container.s-overlay__above > form > button.s-cx-search-input__button > svg")
    button_search.press("Enter")

#výber ručníku a následně zeleneho ručníku
    page.locator("#product_0 > div > div.odsc-tile__inner").click()        
    page.locator("#__nuxt > div > main > section > article > div:nth-child(1) > div:nth-child(2) > div.block.block--mobile-hidden > section > div > ul > li > ul > li:nth-child(3) > label").click()        

#přidání zeleného ručníka do košíku  
    page.locator("#__nuxt > div > main > section > article > div:nth-child(1) > div:nth-child(2) > div.block.block--mobile-hidden > section > div > div.cart-section-one > div.cart-section-one__button.cart-section-one__button--extra-gap > div.button-content > pca-the-button").click()         

#pokračování na platbu  
    page.locator("div > pca-v-button:nth-child(2)").click()     
 
#zvolení objednání bez registrace  
    page.locator("#guest-account-submit").click()       

#kontrola jestli při zvolení objednání bez registrace se objeví chybové hlášky  
    email = page.locator("#app > div > main > div.login-page > section > div.checkout-login-page__container > section:nth-child(3) > form > div:nth-child(1) > div.base-with-validation__validation > div > span")
    email_check = page.locator("#app > div > main > div.login-page > section > div.checkout-login-page__container > section:nth-child(3) > form > div:nth-child(2) > div.base-with-validation__validation > div > span")
    
    assert email.is_visible() == True
    assert email_check.is_visible() == True

    

    










