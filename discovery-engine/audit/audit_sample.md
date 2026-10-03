# Hand audit of 20 AI classifications

The discovery engine tagged 1,196 posts with Gemini. These 20 were drawn
at random, with a fixed seed, from three bands -- including two bands of
rows the model **rejected**, so the audit can catch what the filter threw
away and not only what it wrongly kept.

For each row: read the post, then put `yes` or `no` in **Agree**. If no,
say what the right label was. That is the whole task.

- **Band A** (10 of 84): Classed as a vague-memory retrieval failure (the headline 84)
- **Band B** (5 of 159): Judged relevant, but classed as a different kind of problem
- **Band C** (5 of 953): Judged NOT relevant, and dropped before analysis

---

## 1. Band A · `0c80784a5d16` · app_store

> It makes all manner of fancy stuff - tells you it’s done it then hides it away never to be found.

| field | what the AI said |
|---|---|
| is_relevant | `True` |
| problem_class | `vague_memory_retrieval` |
| failure_stage | `cannot_express` |
| cues_remembered | `[]` |

**Agree:**  
**If no, the right label is:**  

---

## 2. Band A · `955a05734288` · reddit_comment

> I tried that and got no results. I tried "Bob and Sue" and "Bob Sue" and got nothing. Bob alone works great.

| field | what the AI said |
|---|---|
| is_relevant | `True` |
| problem_class | `vague_memory_retrieval` |
| failure_stage | `app_misunderstands` |
| cues_remembered | `['people_present']` |

**Agree:**  
**If no, the right label is:**  

---

## 3. Band A · `5d2b1f997d5e` · app_store

> I can’t always find the videos I’m looking for but it is nice when they just pop up with a new video of memories or wanna make dogs. It’s kind of cool they put it to music. The only thing is I don’t know how really did edit them that well but that’s OK.

| field | what the AI said |
|---|---|
| is_relevant | `True` |
| problem_class | `vague_memory_retrieval` |
| failure_stage | `app_misunderstands` |
| cues_remembered | `['none_stated']` |

**Agree:**  
**If no, the right label is:**  

---

## 4. Band A · `af06b2eb4d35` · play_store

> ​It's impossible to search for a file, by the name of image, on new phone. EXTREMELY STUPID !!!!! When I search, it shows all kinds of garbage/nonsense, instead of the requested images by name. Do not install this app

| field | what the AI said |
|---|---|
| is_relevant | `True` |
| problem_class | `vague_memory_retrieval` |
| failure_stage | `app_misunderstands` |
| cues_remembered | `['text_content']` |

**Agree:**  
**If no, the right label is:**  

---

## 5. Band A · `e68a73391226` · play_store

> Ongoing issue for some time now. It fails to recognise pets in a lot of photos. If I type in search bar "dogs", those pet photos appear, however if I just go through People and Pets, photos do not appear despite turning on the pets function. It recognises some but not others... edit: face groups was turned on and still not working..

| field | what the AI said |
|---|---|
| is_relevant | `True` |
| problem_class | `vague_memory_retrieval` |
| failure_stage | `app_misunderstands` |
| cues_remembered | `['visual_detail']` |

**Agree:**  
**If no, the right label is:**  

---

## 6. Band A · `3bfa12482840` · play_store

> I used to really like this app but things have gotten so confusing that it's nearly impossible to find pictures. I don't understand why sometimes pictures from the cloud show up and sometimes they don't. Why can I not see all my pictures in the main feed? Often I'll save a picture and it will be seemingly nowhere. Screenshots are the worst. The only features I can appreciate are sorting people by face and the AI search to find specific things (when it works).

| field | what the AI said |
|---|---|
| is_relevant | `True` |
| problem_class | `vague_memory_retrieval` |
| failure_stage | `cannot_express` |
| cues_remembered | `['approx_time']` |

**Agree:**  
**If no, the right label is:**  

---

## 7. Band A · `bcac88013612` · play_store

> I absolutely hate the AI thing. I can't find photos as easily as I used to never the ai thing always had a damn issue finding it! it's literally ARTIFICIAL INTELLIGENCE but it can't do anything. put it back to how it used to be!

| field | what the AI said |
|---|---|
| is_relevant | `True` |
| problem_class | `vague_memory_retrieval` |
| failure_stage | `app_misunderstands` |
| cues_remembered | `['none_stated']` |

**Agree:**  
**If no, the right label is:**  

---

## 8. Band A · `ef44f1a40576` · reddit_post

> Just last week, Google Photos search was awesome. Need a pic of passport? Just type "Passport". Forgot your Known Traveler Number? Search "Global Entry Card". Now I search any of the above and it shows be thousands of photos with absolutely no relevance. What happened?

| field | what the AI said |
|---|---|
| is_relevant | `True` |
| problem_class | `vague_memory_retrieval` |
| failure_stage | `app_misunderstands` |
| cues_remembered | `['text_content']` |

**Agree:**  
**If no, the right label is:**  

---

## 9. Band A · `cfb3fa885841` · play_store

> Photos used to be the perfect photos app. it had the best search funding of any app. I used to race iphone users to see how far we could find the same photo and I always won. Now this near perfect search function has been replaced by AI, which not only doesn't return the photos I'm looking for, it actually acts as a stumbling block to me finding them. It's slow and inefficient. Another perfectly good tool ruined in the name of trying to convince us that AI is inevitable.

| field | what the AI said |
|---|---|
| is_relevant | `True` |
| problem_class | `vague_memory_retrieval` |
| failure_stage | `app_misunderstands` |
| cues_remembered | `['none_stated']` |

**Agree:**  
**If no, the right label is:**  

---

## 10. Band A · `66818886c57a` · play_store

> Worse with every update. Can't find anything. Constantly tries to make me turn on the auto backup despite repeatedly saying no. Bonus for constantly trying to show Gemini where no one wants it.

| field | what the AI said |
|---|---|
| is_relevant | `True` |
| problem_class | `vague_memory_retrieval` |
| failure_stage | `app_misunderstands` |
| cues_remembered | `[]` |

**Agree:**  
**If no, the right label is:**  

---

## 11. Band B · `175325cbcd66` · reddit_comment

> Google photos was critical to our business. We take photos and make albums of locations and sites. Being able to go back to the album to review the photos is essential for us. We have tons of documents that contain links to those albums. We did that using Google photos for eight years. Then, this summer Google permanently broke approximately 30 percent of all of those albums. The link gives an error "there's nothing here" If you navigate to the albums in the account that created it, same thing "this album is empty". This has been crushing us this year. the photos exist, but there is no way to put them back into order accurately. Its almost easier to book a flight, hotel, rental car and go ba …

| field | what the AI said |
|---|---|
| is_relevant | `True` |
| problem_class | `data_missing_sync` |
| failure_stage | `content_not_indexed` |
| cues_remembered | `['context_event']` |

**Agree:**  
**If no, the right label is:**  

---

## 12. Band B · `0918fc6d3aa0` · play_store

> The new Google Photos update is honestly very disappointing. The previous version was much more convenient and user-friendly. The “Search by People” option, which was one of the most useful features, is now missing or difficult to find. Why remove or hide a feature that made finding specific photos so easy? The new update feels more complicated instead of being an improvement. Please bring back the “Search by People” option and make the app as convenient as it was before.

| field | what the AI said |
|---|---|
| is_relevant | `True` |
| problem_class | `ui_navigation_regression` |
| failure_stage | `cannot_express` |
| cues_remembered | `['people_present']` |

**Agree:**  
**If no, the right label is:**  

---

## 13. Band B · `e18f72f4359a` · play_store

> I like Google photos but the mobile app is a bit of a cluster compared to the more straightforward, less clustered desktop/PC version. Also, is there a reliable way for duplicate images to be axed without having to manually check to make sure you're not deleting both? I'm talking for like 100s+ of pictures. Thanks! edit 8/28/26, why are my photos not showing up in the big main page? Only some are, the rest are on Recently Added. Having to go dig for my most recent screenshots is nuts

| field | what the AI said |
|---|---|
| is_relevant | `True` |
| problem_class | `ui_navigation_regression` |
| failure_stage | `app_misunderstands` |
| cues_remembered | `['approx_time', 'source_channel']` |

**Agree:**  
**If no, the right label is:**  

---

## 14. Band B · `4c54c48c0ec1` · app_store

> Would love if app layout could go back to monthly sections as photos are so hard to find now that they are all cluttered together which makes the app much harder to use

| field | what the AI said |
|---|---|
| is_relevant | `True` |
| problem_class | `ui_navigation_regression` |
| failure_stage | `cannot_express` |
| cues_remembered | `['approx_time']` |

**Agree:**  
**If no, the right label is:**  

---

## 15. Band B · `1aae247d3e7c` · play_store

> Hate the update, no longer able to search without using Gemini, which I also hate. Have disabled Gemini, because I couldn't search anything, without it popping up several times, even though I had already said no, and closed it. *Editing to add, since there's no way to reply to your reply. Ask photos also requires Gemini, so that doesn't help at all. Thanks for nothing 👍🏻

| field | what the AI said |
|---|---|
| is_relevant | `True` |
| problem_class | `ui_navigation_regression` |
| failure_stage | `cannot_express` |
| cues_remembered | `[]` |

**Agree:**  
**If no, the right label is:**  

---

## 16. Band C · `04f2969bffbd` · play_store

> A very good app with a lot of features I enjoy very much but there's this problem I discovered recently and it's annoying,all my photos and videos where backed up with it's original quality I had to reset my phone due to some circumstances,and my pictures were backed up so after all and all I restored my pictures and videos only to find out that they were not restored to it's original quality 😕 which is not supposed to be so!!!! and it's annoying 😔 but nonetheless a great app and the very best

| field | what the AI said |
|---|---|
| is_relevant | `False` |
| problem_class | `` |
| failure_stage | `not_applicable` |
| cues_remembered | `[]` |

**Agree:**  
**If no, the right label is:**  

---

## 17. Band C · `e34b0bb2043b` · reddit_comment

> I did the same thing 😔 came here looking for help

| field | what the AI said |
|---|---|
| is_relevant | `False` |
| problem_class | `` |
| failure_stage | `not_applicable` |
| cues_remembered | `[]` |

**Agree:**  
**If no, the right label is:**  

---

## 18. Band C · `b1016eabe23d` · app_store

> Changed my 5 star to 2 star. I have trusted this since Picasa days but honestly I’m forced to explore other solutions because Google Photos has become SO SLOW. Every time I open the app it takes forever to load any photos. Nothing seems cached at all. Adding individual photos to an album? It takes up to 7 seconds to retrieve the list of albums every.. single.. time. It’s a painful process. Are you guys not watching your system dashboards? I’ve even wiped my device and started clean to see if that helps things, but there seem to have been some architectural changes on Google’s side for the worse over the years. It may be fine for small collections but with 2TB and 70k photos this is borderlin …

| field | what the AI said |
|---|---|
| is_relevant | `False` |
| problem_class | `` |
| failure_stage | `not_applicable` |
| cues_remembered | `[]` |

**Agree:**  
**If no, the right label is:**  

---

## 19. Band C · `12d3271751bd` · reddit_comment

> ^^^^^^^^This is how you respond when you have technical knowledge and information of use. I don't want to sound sarcastic at all, please don't mistake me, I'm being completely genuine, you can see in the rest of the thread why I might want to make this abundantly clear. Thank you for not being an absolute dick and actually having something to add and being willing to share it. I did do what you said in Explorer, despite what that other guy is insisting, but toffee dates are completely wrong and exactly the same for every file. I've put every single date column on, including that one, and none of them are the correct dates. They are just the various dates that changes have been made, like dow …

| field | what the AI said |
|---|---|
| is_relevant | `False` |
| problem_class | `` |
| failure_stage | `not_applicable` |
| cues_remembered | `[]` |

**Agree:**  
**If no, the right label is:**  

---

## 20. Band C · `b799b74ebe16` · reddit_post

> Hello and welcome to the other side of the bricks. **This is a starter guide for everyone who wants to buy any types of bricks, building blocks or minifigures from China.** It's a reworked version of [the previous guide](https://www.reddit.com/r/lepin/comments/gfq2lo/kingqueenjack_formerly_lepin_starter_guide/). This guide contains everything you need to know and has lots of useful links. List of all guides is available [here](https://www.reddit.com/r/lepin/wiki/guides). # Introduction. This sub was named after one of the most famous knock off bricks company - **Lepin**. **Lepin is shut down** now, but for many people the term "Lepin" means all kind of bricks and sets from chinese companies. …

| field | what the AI said |
|---|---|
| is_relevant | `False` |
| problem_class | `` |
| failure_stage | `not_applicable` |
| cues_remembered | `[]` |

**Agree:**  
**If no, the right label is:**  

---

## Result

Fill these in once every row above has an answer, then put the
agreement line on slide 1.

- Rows audited: 20
- Rows where the human agreed with every field: __ of 20
- Fields corrected: __
- What the disagreements had in common: ____
