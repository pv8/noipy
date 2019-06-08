import mechanicalsoup

def get_dwr921_ip(router_ip, router_user, router_pwd):
    # Connect to Router
    browser = mechanicalsoup.StatefulBrowser()
    browser.open("http://{0}/wanst.htm".format(router_ip))
    # Remplir le formulaire
    browser.select_form('form[name="login"]')
    browser["un"] = router_user
    browser["pw"] = router_pwd
    page = browser.submit_selected()
    # Retour
    return page.soup.find("td", id="ip3g").text
