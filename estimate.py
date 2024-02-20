import main



while True:
    text = input(">>")
    # 获取拼音
    pinyin_of_text = main.get_pinyin(text)
    main.estimate(text, pinyin_of_text, main.model_2d)
