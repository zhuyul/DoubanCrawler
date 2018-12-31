# encoding:utf-8
from selenium import webdriver
import csv

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(chrome_options=options)

    url = inputURL(driver)
    print("Fetching data ...")
    commentDict = crawler(driver, url)
    writeToCsv(commentDict)
    print("Done")

def inputURL(driver):
    while not driver.find_elements_by_class_name("item"):
        user = input("Type Douban user name: ")
        url = "https://movie.douban.com/people/" + user + "/collect"
        driver.get(url)
    return url

def crawler(driver, url):
    commentDict = {}
    endPage = False
    while not endPage:
        driver.get(url)
        length = len (driver.find_elements_by_class_name("item"))
        for i in range (0, length):
            movie_list = driver.find_elements_by_class_name("item")
            movie = movie_list[i]
            title = movie.find_element_by_css_selector("[class='title']").text.rstrip(" [可播放]")
            fetchComments(movie, title, commentDict)
        try:
            url = driver.find_element_by_css_selector("[rel='next']").get_attribute("href")
        except:
            endPage = True
    driver.close()
    return commentDict

def fetchComments(movie, title, commentDict):
    try:
        comment = movie.find_element_by_css_selector("[class='comment']").text
        commentDict[title] = comment
    except:
        pass

def writeToCsv(data):
    csv_file = open("UserComments.csv","w",newline="")
    writer = csv.writer(csv_file)
    writer.writerow(["Title","Comment"])
    for key, value in data.items():
        writer.writerow([key,value])
    csv_file.close()

# NOT USED
# fetch director and genre info on each movie page
def fetchMoviePage(driver, title, movie, genreDict, directorDict):
    movieURL = movie.find_element_by_css_selector("[class='title']").find_element_by_tag_name("a").get_attribute('href')
    driver.get(movieURL)
    movieInfo = driver.find_elements_by_class_name("attrs")
    try:
        directors = movieInfo[0].text
        director = directors.split(' / ')
        for di in director:
            if di not in directorDict:
                directorDict[di] = 1
            else:
                directorDict[di] += 1
        movieGenres = driver.find_elements_by_css_selector("[property='v:genre']")
        for movieGenre in movieGenres:
            genre = movieGenre.text
            if genre not in genreDict:
                genreDict[genre] = 1
            else:
                genreDict[genre] += 1
        driver.back()
    except:
        driver.back()

def findTop(myDict):
    del myDict['']
    for key in myDict.keys():
        myDict[key] = int(myDict[key])
    top = max(myDict.items(), key=lambda k: k[1])
    return top

def fetchUserFiveStarMovie(movie, title, movieURL, fiveStarMoviesDict):
    try:
        if movie.find_element_by_css_selector("[class='rating5-t']"):
            fiveStarMoviesDict[title] = movieURL
    except:
        pass

if __name__ == '__main__':
    main()