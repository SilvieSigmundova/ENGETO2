import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="module")
def browser():
   with sync_playwright() as playwright:
      browser = playwright.firefox.launch(headless=False, slow_mo=5000)
      yield browser
      browser.close()

@pytest.fixture(scope="module")
def page(browser):
   page = browser.new_page()
   page.goto("https://engeto.cz/")
   page.wait_for_load_state()
   yield page
   page.close()

@pytest.fixture(scope="module")
def pageT(browser):
   pageT = browser.new_page()
   pageT.goto("https://engeto.cz/testovani-softwaru/")
   pageT.wait_for_load_state()
   yield pageT
   pageT.close()

#Potvrzení Cookies
def cookies(page):
   accept_button = page.locator('text="Chápu a přijímám!"').is_visible()
   if accept_button == False:
      print("Cookies se nezobrazily nebo nebyly potvrzeny.")
   else:
      accept_button.click()
      print("Cookies potvrzeny.")





def test_scenario_prvni(page):
   print("TEST1: Začátek testu.")
   cookies(page)

   menu3=page.get_by_role("link", name="FAQ", exact=True)
   menu3.click()

   uradp=page.locator("label[for='filter-item_urad-prace']").locator("text='Úřad práce – proplacení kurzu'")
   uradp.click()

   linkup=page.locator("a[href='#urad-prace-jak-funguji-prispevky-na-vase-kurzy']")
   linkup.click()

   # Kontrola, zda funguje odkaz na MPSV.
   mpsv=page.locator("a[href='https://www.mpsv.cz/']")
   mpsv.click()
   pageurl=page.url
   if pageurl=='https://www.mpsv.cz/':
      print("TEST1: Přesun na stránku MPSV se zdařil.")
   else:
      print("TEST1: Přesun na stránku MPSV se nezdařil.")
   page.go_back()

   # Kontrola, zda funguje odkaz na žádost o zařazení do evidence zájemců o zaměstnání u MPSV.
   linkup2=page.locator("a[href='#urad-prace-jake-jsou-podminky-prihlaseni']")
   linkup2.click()

   mpsv2=page.locator("a[href='https://www.mpsv.cz/zadost-o-zarazeni-do-evidence-zajemcu-o-zamestnani']")
   mpsv2.click()
   
   titulmpsv=page.is_visible("text='Žádost o zařazení do evidence zájemců o zaměstnání'")
   if titulmpsv == True:
      print("TEST1: Přesměrování na žádost MPSV proběhla v pořádku.")
   else:
      print("TEST1: Přesměrování na žádost MPSV neproběhla v pořádku.")
   page.go_back()
   lo=page.locator("#logo").click()
   print("TEST1: Konec testu.")




def test_scenario_druhy(page):
   print("TEST2: Začátek testu.")
   cookies(page)

   #Kontrola titulku.
   title_2=page.title()
   if title_2 == "Kurzy programování a dalších IT technologií | ENGETO":
      print("TEST2: Titulek se shoduje.")
   else:
      print("TEST2: Titulek se neshoduje.")

   menu=page.get_by_role("link", name="Kurzy")
   menu.click()

   menu2=page.get_by_role("link", name='Testing Akademie | ENGETO Testing Akademie')
   menu2.click()

   plan_button=page.locator('text="Zobrazit celý studijní plán"')
   plan_button.click()

   #Kontrola, zda se rozbalí přehled lekcí.
   lekce=page.locator('text="11. lekce"').is_visible()
   if lekce==True:
      print("TEST2: Seznam lekcí se rozbalil.")
   else:
      print("TEST2: Seznam lekcí se nerozbalil.")                         

   page.get_by_alt_text("ENGETO Academy").click()

   #Kontrola návratu přes ikonku Engeta.
   title_3=page.title()
   if title_3 == "Kurzy programování a dalších IT technologií | ENGETO":
      print("TEST2: Návrat na domovskou stránku přes logo proběhl.")
   else:
      print("TEST2: Návrat na domovskou stránku přes logo se neproběhl")
   print("TEST2: Konec testu.")




def test_scenario_treti(page):
   print("TEST3: Začátek testu.")
   cookies(page)

   t1=page.get_by_role("link", name='Přehled IT kurzů')
   t1.click()

   #Kontrola titulku.
   title_3=page.title()
   if title_3 == "Kurzy programování s lektorem | Dotace až 50 000 Kč":
      print('TEST3: Stránka s přehledem kurzů se zobrazila.')
   else:
      print('TEST3: Stránka s přehledem kurzů se nezobrazila.')

   t2=page.get_by_role("link", name='Tester s Pythonem Už jen')
   t2.click()

   #Kontrola přes titulek, že se vybrat správný kurz.
   title_4=page.title()
   if title_4 == "Kurz: Software tester s Pythonem | ENGETO":
      print('TEST3: Kurz "Tester s Pythonem" byl vybrán správně.')
   else:
      print('TEST3: Kurz "Tester s Pythonem" nebyl vybrán správně, zkontrolujte test.')
   
   t3=page.locator("text='Detail termínu'")
   t3.nth(0).click()

   t4=page.get_by_role("link", name='Objednat kurz')
   t4.click()

   cenacelkem1=page.locator("span.woocommerce-Price-amount.amount").nth(0).text_content()
   cenacelkem_1=(int(cenacelkem1.replace(" ","").replace("Kč","")))*2

   pl=page.locator(".plus.flex-as-s.flex.flex-ai-c")
   pl.click()

   cenacelkem2=page.locator("span.woocommerce-Price-amount.amount").nth(0).text_content()
   cenacelkem_2=int(cenacelkem2.replace(" ","").replace("Kč",""))

   #Kontrola, že souhlasí částka, když se změní počet kurzů na 2.
   if cenacelkem_1==cenacelkem_2:
      print("TEST3: Cena celkem souhlasí.")
   else:
      print("TEST3: Cena celkem nesouhlasí.")

   t5=page.locator("text='Pokračovat v objednávce'")
   t5.click()

   #Kontrola, že se zobrazuje objednávkový formulář pro fyzickou osobu.
   fo1=page.locator("#billing_first_name").is_visible()
   fo2=page.locator("#billing_last_name").is_visible()
   if fo1==True and fo2==True:
      print("TEST3: Jsou zobrazeny fakturační údaje pro fyzickou osobu.")

   #Kontrola, že se zobrazuje objednávkový formulář pro právnickou osobu.
   ch1=page.locator(".checkbox").locator("text='Nakupuji na firmu'")
   ch1.click()

   po1=page.locator("#billing_ico").is_visible()
   po2=page.locator("#billing_vat").is_visible()

   if po1==True and po2==True:
      print("TEST3: Jsou zobrazeny fakturační údaje pro právnickou osobu.")
 
   print("TEST3: Konec testu.")




@pytest.mark.parametrize(
   "atribut, sekce",
   [
      ("#co_se_naucis", "Co se naučíš?"),
      ("#prubeh_kurzu", "Průběh kurzu"),
      ("#studijni_plan", "Studijní plán"),
      ("#cile_kurzu", "Cíle kurzu"),
      ("#proc_studovat_u_nas", "Proč studovat u nás?"),
      ("#lektori", "Lektoři"),
      ("#pribehy_a_reference", "Příběhy a reference"),
      ("#faq", "Často kladené otázky"),
      ("#terminy", "Termíny"),
   ],
)

#Kontrola, zda na detailu kurzu Testing Akademie existují dané sekce.
def test_nazvy_sekci(pageT,atribut,sekce):   
   atrsek = pageT.locator(f"a[href='{atribut}']").locator(f"text='{sekce}'")
   
   if (atrsek.count()>=1):
      print(f"Sekce \"{sekce}\" kurzu Testing Akademie existuje.")
   else:
      print(f"Sekce \"{sekce}\" kurzu Testing Akademie neexistuje.")