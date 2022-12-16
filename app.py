from menu import Menu

if __name__ == "__main__":
    try:
        Menu().show_menu()
    except Exception as e:
        print(e)
        print("Error occured!")
    finally:
        print("Goodbye!")
