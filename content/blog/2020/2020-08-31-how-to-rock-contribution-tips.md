+++
title = 'How to rock: Doing the right thing'
date = 2020-08-31T13:55:39z
[taxonomies]
tags = [ "how-to-rock", "kde", "development", "tutorial" ]
[extra]
header = "/assets/how_to_rock/maintain.jpg"
+++

After a couple of years collaborating with open source/free software projects, I started to help newcomers to contribute and push the development practices further. This post will try to itemize the most important items that can used for software collaboration.
Before starting, be sure to follow my [previous posts](/tags/how-to-rock), this post complements what already exists.


<!-- more -->
Now, I'm going to throw some good practices of code development and contribution, and during this post I'll explain why such practices can be archived without much effort:

- **Avoid creating multiple PRs for the same work**, update the ones that are still open.
  - E.g: You created a Pull Request called "Feature: add button", some modifications will be necessary after the review process, and for that you'll need to update the same branch over creating new ones. That's necessary to help the project maintainers to see previous comments and your development history, avoid repository noise and unnecessary PRs in the project history. Creating multiple PRs will only make the maintainers confuse and unable to track old comments, suggestions and your code changes between PRs.

- **Create atomic and self-contained commits**, avoid doing multiple things in the same commit.
  - E.g: You have created a commit to fix the serial communication class, and inside the same commit you are doing 3 different things, removing trailing spaces, fixing a pointer validation check and a typo in the documentation of a totally different class. This can appear to be silly and bureaucratic, but there are good reasons to break this simple commit and at least 3 different commits, one for the pointer check, a second one for the typo and a third one for the trailing space.
      - It makes your work more clear when the maintainer does the review per commit
      - Makes it easier for developers to cherry-pick your work avoiding conflicts
      - Makes it easier to fix conflicts when doing rebases over the master branch
      - - Helps developers to read the project history
        - Developers usually track lines history to understand the changes behind a functionality, it's common to search with `git grep` history from commits or lines changes in specific commits to understand the code, function, class or a small feature.

- **Create atomic and self-sustained PRs**, avoid doing multiple things in the same PR, like different features. They may appear simple with small pieces of code/functionality but they can escalate quickly after a review process, and if both features are somehow related or dependently, it's recommended to break it in multiple PRs with code to maintain compatibility with current code base. A huge PR can drag developer and maintainer in a rabbit hole, making the PR to be not merged, keeping it simple is the best way to merge it and get the sweet serotonin boost.
  - E.g: You have applied a PR for software notifications, and somehow you also added a URL fetch functionality to grab new software versions, etc. After the first review, the maintainer asks to create a more abstracted way to fetch api and to deal with network requirements, this will start to convolute the PR, moving the initial idea of the notification feature to an entire network REST API architecture. With that, it's better to break the PR in two, one that only provides the notification software and interface feature and a second PR that is used for the REST API.

- **Do your own review**, the final and probably most important tip of all. Doing you own review will train your mind and eyes to detect poor code standards or bad practices, it'll also make your PR be merged easily and faster, since you'll be able to catch problems before the reviewer feedback. Some reviewers may think that reviewing your own PR is a must, since we are talking about open source projects and free software, you should understand that the people that are reviewing your code are not obligated to do so, the majority are collaborating and donating their own time to help the development and maintenance of such projects, doing your own review is also sign of empathy about the project and maintainer time.