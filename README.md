# autofill_nuist
Autofill questionnaires or others released by NUSIT

Drivers can be downloaded from Third Party Drivers, Bindings, and Plugins of https://www.seleniumhq.org/download/. These scripts use Google Chrome Driver.

1. academic_morality

   - crawl answers (optional)

     ```
     # change driver_path to the path of driver
     $ python crawl_ans.py
     ```

     ![academic_morality](https://github.com/zxdawn/autofill_nuist/raw/master/examples/academic_morality_1.gif)

   - answer the questionnaire

     ```
     # change driver_path to the path of driver
     $ python ans_form.py
     ```

     ![academic_morality](https://github.com/zxdawn/autofill_nuist/raw/master/examples/academic_morality_2.gif)