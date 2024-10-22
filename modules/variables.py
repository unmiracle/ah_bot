from multiprocessing import Value


class Config:
    catched = 0

    running = Value('b', True)
    is_buy_enabled = Value('b', True)

    afk_timeout_min = 20

    pixels_offset = 70

    # locations
    auction_house_btn = (2290, 380)
    first_item_btn = (2025, 485)
    reset_btn = (2340, 323)
    count_from_location = (2334, 510)

    item_header_text = (810, 494)


    # delays
    monitor_delay = 0.02
    reset_click_delay = 0.01


    # colors
    item_header_color = (169, 121, 203)
    default_bg_color = (28, 26, 37)