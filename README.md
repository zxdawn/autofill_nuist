# autofill_nuist
Autofill questionnaires or others released by NUSIT

Drivers can be downloaded from Third Party Drivers, Bindings, and Plugins of https://www.seleniumhq.org/download/. These scripts use Google Chrome Driver.

1. academic_morality

   change driver_path in scripts to the path of driver

   - crawl answers (optional)

     ```
     $ python crawl_ans.py
     ```

     ![academic_morality](https://github.com/zxdawn/autofill_nuist/raw/master/examples/academic_morality_1.gif)

   - answer the questionnaire

     ```
     $ python ans_form.py
     ```

     ![academic_morality](https://github.com/zxdawn/autofill_nuist/raw/master/examples/academic_morality_2.gif)