if __name__ == "__main__":
    import os
    if os.environ.get("GMAPS_GUI_LAUNCHED") != "yes":
        os.environ["GMAPS_GUI_LAUNCHED"] = "yes"
        from gmaps.gui import ScraperGUI
        ScraperGUI().mainloop()