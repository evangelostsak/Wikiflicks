import random
from imdb import Cinemagoer
import wikipedia
from colorama import Fore, Style, init
from PIL import Image
from difflib import SequenceMatcher

# Initialize colorama for colored text output
init(autoreset=True)

# Initialize IMDb object
ia = Cinemagoer()


def display_image(image_path, width=None, height=None):
    """Display an image when the player wins, retries, or loses."""
    try:
        img = Image.open(image_path)

        # Resize the image if width and height are provided
        if width and height:
            img = img.resize((width, height))

            img.show()
    except Exception as e:
        pass


def similar(str1, str2):
    """Compare the similarity between two strings."""
    return SequenceMatcher(None, str1, str2).ratio()


def get_movie_title():
    """Retrieve a random title from IMDb's top 250 movies."""
    try:
        movies = ia.get_top250_movies()  # Retrieve the top 250 movies
    except Exception as error:
        print(f"Error fetching top 250 movies: {error}")
        return None
    if not movies:
        print("No movies were retrieved from IMDb.")
        return None
    random_movie = random.choice(movies)
    return random_movie['title']


def get_plot(movie_title):
    """Extract the plot summary from Wikipedia."""
    search_result = wikipedia.search(movie_title)
    if len(search_result) == 0:
        print(f"Couldn't find anything for {movie_title}")
        return None

    for result in search_result:
        try:
            summary_page = wikipedia.page(result)

            # Check if the page is about a movie
            if "film" in summary_page.title.lower() or "movie" in summary_page.title.lower():
                plot_section = summary_page.section("Plot")
                if plot_section:
                    # Limit the plot to the first 150 words
                    plot_words = plot_section.split()[:150]
                    return ' '.join(plot_words) + '...'
                else:
                    print(f"No 'Plot' section found for {result}.")
                    return None

            content = summary_page.content.lower()
            if "film" in content[:500]:
                plot_section = summary_page.section("Plot")
                if plot_section:

                    # Limit the plot to the first 150 words
                    plot_words = plot_section.split()[:150]
                    return ' '.join(plot_words) + '...'
        except wikipedia.exceptions.DisambiguationError:
            pass
            continue
        except wikipedia.exceptions.PageError:
            pass
            continue
    return None


def start_game():
    """The game logic with score, retries, and image displays."""
    stars = "★" * 3
    print(Fore.LIGHTWHITE_EX + stars + Fore.LIGHTYELLOW_EX + Style.BRIGHT + " WELCOME TO WikiFlicks! 😊🎬 " + Fore.LIGHTWHITE_EX + stars)
    print(Fore.LIGHTWHITE_EX + "★ " + Fore.LIGHTYELLOW_EX + "The game for Cinephiles who can name the movie from a single Wikipedia clue! 📽️" + Fore.LIGHTWHITE_EX + " ★")
    print(Fore.LIGHTWHITE_EX + "You will be given a snippet from a movie, and you should write the movie's title. 📝")
    print(Fore.LIGHTWHITE_EX + "If you're right, you'll earn 10 points!")
    print(Fore.LIGHTWHITE_EX + "Every wrong answer costs you 5 points. Be careful!")

    total_score = 0
    incorrect_rounds = 0
    incorrect_tries = 0
    max_rounds  = 3
    lifes = 3
    asked_movies = set()

    while incorrect_rounds < max_rounds:
        print("\n" + Fore.YELLOW + "Loading movie... 🎥")
        movie_title = get_movie_title()
        if not movie_title or movie_title in asked_movies:
            continue
        asked_movies.add(movie_title)

        summary = get_plot(movie_title)
        if not summary:
            print(f"Couldn't retrieve the summary for {movie_title}. Skipping to the next movie.")
            continue
        print(f"You have {lifes} left: ")
        while True:
            # Guess prompt
            print(Fore.LIGHTYELLOW_EX + "Can you guess the flick? 🤔")
            print(Fore.CYAN + summary)

            user_guess = input(Fore.LIGHTYELLOW_EX + "What is your guess? ").strip()
            similarity = similar(user_guess.lower(), movie_title.lower())

            if similarity >= 0.85:
                total_score += 10
                # Success message
                print(Fore.GREEN + f"Congrats! 🎉 You've earned 10 points. Total score: {total_score} 😎")
                print(Fore.GREEN + f"You gave the correct answer: {movie_title}")
                display_image("win_image.png")  # Display winning image
                break
            else:
                if total_score == 0:
                    print(Fore.RED + f"Not quite... Try again!😞")
                    print(Fore.RED + f"Total score: {total_score} 📝")
                    incorrect_tries += 1
                    display_image("try_again_image.png")  # Display try again image
                    if incorrect_tries == 3:
                        print(Fore.RED + f"Sorry, the correct answer was: {movie_title} 😞")
                        incorrect_rounds += 1
                        incorrect_tries -= 3
                        lifes -= 1
                        break

                else:
                    total_score -= 5
                    print(Fore.RED + f"Not quite... Try again! 😞")
                    print(Fore.LIGHTWHITE_EX + f"Total score: {total_score} 📝")
                    incorrect_tries += 1
                    display_image("try_again_image.png")  # Display try again image
                    if incorrect_tries == 3:
                        print(Fore.RED + f"Sorry, the correct answer was: {movie_title} 😞")
                        incorrect_rounds += 1
                        incorrect_tries -= 3
                        lifes -= 1
                        break

        if incorrect_rounds < max_rounds:
            continue_game = input(Fore.LIGHTWHITE_EX + "Do you want to play another round? (yes/no) 😊🍀: ").strip().lower()
            if continue_game == "yes":
                print(Fore.LIGHTWHITE_EX + "Loading new movie. Please wait... 🎬")

            elif continue_game == "no":
                if total_score == 0:
                    print(Fore.RED + "Game over! Better luck next time. 😢")
                    display_image("lose_image.png")  # Display losing image
                    break
                else:
                    print(Fore.CYAN + "Thanks for playing! 🎉")
                    print(Fore.CYAN + f"You scored {total_score} points. 🏆")
                    print(Fore.CYAN + "Take care!")
                    break

        if incorrect_rounds == max_rounds:
            if total_score == 0:
                print(Fore.RED + "Game over! Better luck next time. 😢")
                display_image("lose_image.png")  # Display losing image
                break
            else:
                print(Fore.CYAN + "Thanks for playing! 🎉")
                print(Fore.CYAN + f"You scored {total_score} points. 🏆")
                print(Fore.CYAN + "Take care!")
                break


def main():
    start_game()


if __name__ == "__main__":
    main()