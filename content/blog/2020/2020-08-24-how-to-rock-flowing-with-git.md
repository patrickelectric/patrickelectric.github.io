+++
title = 'How to rock: Flowing with git'
date = 2020-08-24T13:55:39z
draft = false
[taxonomies]
tags = [ "kde", "development", "tutorial", "how-to-rock" ]
[extra]
header = "/assets/how_to_rock/banner-flowing-with-git.jpg"
+++

Git is awesome, git rocks, git is like a super advanced car, but if you don't read the manual, you'll never know the features!

The idea behind this section is to point some important things that I learned in the pass years while reading some great books, such as: [Mastering Git](https://isbnsearch.org/isbn/9781783553754) and [Pro Git(it's free!)](https://git-scm.com/book/en/v2).

Hopefully, after going through this post, you'll be able to improve your understanding about git, and how to flow correctly with its concept.

> Note: This is not an introductory post, there is a bunch of great guides in google about it, but it should help you to get the big picture.

<!-- more -->

# Useful tips

Git is awesome, git rocks, git is like a super advanced car, but if you don't read the manual, you'll never know the features!

The idea behind this section is to point some important things that I learned in the pass years while reading some great books, such as: [Mastering Git](https://isbnsearch.org/isbn/9781783553754) and [Pro Git(it's free!)](https://git-scm.com/book/en/v2).

## Tig

Git is really great, but what matters a great tool if the user interface is not as polished as we desire to be. **`Tig`** is one of the greatest tools to be used with Git, is the UI that mostly programmers are missing to visualize and understand what is going on in the git repository. If you didn't know about it, install and use it now.

{% img(url="/assets/how_to_rock/tig-all.png") %}
 tig --all
{% end %}

`Tig` also allow a bunch of useful arguments, such as `log`, `show`, `status`, `reflog`, `blame`, `grep`, `refs`, `stash` and others, we are going to talk about some of these later.

## Git rebase -i (Interactive rebase)

Interactive rebase is a powerful command, and much more powerful and human friend with interactive mode.

## Git reflog

`git reflog` is one of the most important commands, it provides access to everything that is tracked or was tracked by git, all commands and actions that was done in the entire history of the project can be accessed, it's possible to checkout and see the history of development tree in any moment, before or during a rebase, the history of a branch before a terrible idea in the code, a point between a merge conflict, everything is possible to recover or to start from a previous point, if you have done any git command with tracked files, you'll not loose it.

For an awesome experience, I recommend to use `tig` with `reflog` (`tig reflog`) to see a user-friendly history of `reflog`.

{% img(url="/assets/how_to_rock/tig-reflog.png") %}
checkout, rebase, reset, cherry-pick, the history is all there and you can checkout in any hash!
{% end %}

## Git add/checkout/stash --patch/-p

{% img(url="/assets/how_to_rock/add-p.png") %}
git add -p, add only what you need
{% end %}

The `--patch` argument is a great feature, you can use it with `add`, `checkout`, `stash` and others, it allows your to select what you need in your commit,
it helps to avoid adding unnecessary stuff in your commit and only adding what is needed for an atomic patch.

## Git stash

Sometimes we want to remove everything that we are working on, a bunch of uncommitted or unstaged code around your project, but at the same time, we are a big afraid to remove and loose all this code. The answer for your problems is git stash, git will get everything that is not staged.

To visualize what was stashed, you can run `git stash show stash@{0} --all` where `0` can be the nth stash. You can also visualize it with `tig stash`;

If you want to apply any stashed code, you can do it with `git stash apply stash@{0}`, again, where `0` can be the nth stash.

## Git cherry-pick

If you want to test some commits or apply in different branches for any reason, `git cherry-pick` is here for you, with it you can

# Knowing the basic (How the flow works)

> This part was the first section of this post, but since I went really deep about how git works, it's now in the end as a bonus section.

> An alternative title could be: 'Introduction to Git flow', I hope that you understand what kind of introduction I'm talking about :)

Well, if you thought about 'the flow' as related to branches, I can't blame you. First we need to go to the basics, before branches, before anything else.

First we need to create the foundation (`git init`) for our building (our project/source code).

What init will do ? You may ask, well, it creates a folder with a bunch of cool things inside.

```fish
 /tmp/echo (master): tree -a
.
└── .git # Folder where git will store all necessary information to work
    ├── branches # Deprecated, only exist for compatibility
    ├── config # Folder for specific configuration files (~/.gitconfig friends)
    ├── description # Used for GitWeb
    ├── HEAD # A file that has the reference of the current branch (ref/heads/master)
    ├── hooks # Git hook files (comes with bunch of free examples by default), soon we'll talk more about it
    │   ├── applypatch-msg.sample
    │   ├── commit-msg.sample
    │   ├── fsmonitor-watchman.sample
    │   ├── post-update.sample
    │   ├── pre-applypatch.sample
    │   ├── pre-commit.sample
    │   ├── pre-merge-commit.sample
    │   ├── prepare-commit-msg.sample
    │   ├── pre-push.sample
    │   ├── pre-rebase.sample
    │   ├── pre-receive.sample
    │   └── update.sample
    ├── index # Store information related to folders, files and submodules (it'll be populated after you add the first file)
    ├── info # Store information related to a gitignore, gitattributes and etc, we're not going to talk about it
    │   └── exclude
    ├── objects # All our references will be here, soon we are going to see how and what
    │   ├── info # Bunch of internal things that are stored, not going to talk about it
    │   └── pack # Store compressed files, not going to talk about it
    └── refs # All friend references are here, branches, remotes, tags, stags
        ├── heads # Local branches
        ├── remotes # Remote repositories (it'll be populated after you add the first remote)
        │   └── origin # Remote name
        │       └── master # Has the hash of the remote master branch
        └── tags # Store all tags of your project
```

I have added some stuff that are not populated from a fresh `git init` for educational reasons, for more information, check [gitrepository-layout](https://git-scm.com/docs/gitrepository-layout).

Ok, looks complicated right ? It may, but it's not. If you are not aware, `git` description is: "the stupid content tracker",
I believe that may be a weird thing to describe our magical tool with such words, I prefer to say: "the *simple* content tracker", and will explain why.

## Create and add a file

Let's populate our repository and create a simple commit:

1. Create a file: `touch README.md`
2. Let put something inside to make it more funny.
    - `cat README.md`
    ```txt
    Hello!
    ```
    - Now our working directory is not empty, we have something there! But sadly, not tracked by git, we can change that.
3. Add this files to be tracked by git, or indexed: `git add README.md`
4. Wait a minute, we did something with git right ? Let's see what changed:
    ````fish
    .git
    |   ...
    ├── index # It's populated now
    ├── objects # Wow we have some crazy file and folder inside
    │   ├── 10
    │   │   └── ddd6d257e01349d514541981aeecea6b2e741d
    │   ├── info
    │   └── pack
    └── refs
        ├── heads
        └── tags
    ````

## Index

This file is just a binary glob with a bunch of basic information about the files and paths that git is tracking.

What is important for us now, index will have the following content:

1. A header for git internal usage.
2. The number of indexes (hashes) available.
3. A list of hashes that contain:
   1. The filename
   2. The path
   3. The time that the file was changed
   4. Type of the file (can be a folder, or a virtual file and etc)
   5. The permission of such file ([linux permission](https://wiki.archlinux.org/index.php/File_permissions_and_attributes_))
   6. File size
   7. And finally, **our hash (sha1)** [10ddd6d257e01349d514541981aeecea6b2e741d]

Wait, don't you believe me ? Check it here:

```bash
cat index | hx
0x000000: 0x44 0x49 0x52 0x43 0x00 0x00 0x00 0x02 0x00 0x00 DIRC......
0x00000a: 0x00 0x01 0x5f 0x41 0x44 0x35 0x1b 0xd6 0x67 0x47 .._AD5..gG
0x000014: 0x5f 0x41 0x44 0x35 0x1b 0xd6 0x67 0x47 0x00 0x00 _AD5..gG..
0x00001e: 0x00 0x2f 0x00 0x09 0xb1 0x41 0x00 0x00 0x81 0xa4 ./...A....
0x000028: 0x00 0x00 0x03 0xe8 0x00 0x00 0x03 0xe8 0x00 0x00 ..........
0x000032: 0x00 0x07 0x10 0xdd 0xd6 0xd2 0x57 0xe0 0x13 0x49 ......W..I
0x00003c: 0xd5 0x14 0x54 0x19 0x81 0xae 0xec 0xea 0x6b 0x2e ..T.....k.
0x000046: 0x74 0x1d 0x00 0x09 0x52 0x45 0x41 0x44 0x4d 0x45 t...README
0x000050: 0x2e 0x6d 0x64 0x00 0x87 0x87 0x7d 0xde 0xf5 0x59 .md...}..Y
0x00005a: 0x22 0x0a 0x7d 0x9c 0x48 0xce 0xde 0x29 0x94 0x60 ".}.H..).`
0x000064: 0x17 0x2c 0xf3 0xcc                               .,..
   bytes: 104
```

Check `0x000032` until `0x000046`, you'll see our sha1 value **10ddd6d257e01349d514541981aeecea6b2e741d** (*0x10 0xdd 0xd6 0xd2*) and after that our file **README.md**.


If you want to learn how it works and what is inside, check [here](https://git-scm.com/docs/index-format) for more information,
and [here](https://mincong.io/2018/04/28/git-index/) for an awesome adventure.

## Objects

Ok, now that we know that *index* is pointing to this hash, let's check the objects folder.
As I said before, **objects** folder will store all the references that exist, it should be our yellow pages. First, let's understand how to read it.
There is a folder called **10**, and after that a file that has the name of **ddd6d257e01349d514541981aeecea6b2e741d**, if you put both together you are going to end up with our hash that we found in the *index* file.

Just for our curiosity, this hash is calculated based in the following format `{TYPE} {SIZE}{NULL_CHAR}{CONTENT}`, the type will tell git if the hash points to a tree or a blob, the tree can have multiple blobs (like a folder), and a blob is a file. In our case, the string that defines this hash is the following:

```python
import hashlib
hashlib.sha1(b'blob 7\0Hello!\n').hexdigest()
'10ddd6d257e01349d514541981aeecea6b2e741d'
```

For more information, [check Git Internals Git Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects), it's a great friday night reading.


Ok! Now we are ready to commit!

Hey, wait, what is inside of this files object files ?
Oh my, ok, for now, this is where the git magic happens, it's a binary object that contains information about the diff, don't bother about it, but if you are really willing to know, [check it here](https://github.com/gitster/git/blob/master/Documentation/technical/pack-format.txt) (Please open an issue if you know a better and friendly reference).

Back to the commit!

## Commit

1. `git commit -sm "First commit"`

````fish
.git
|   ...
├── index # It's populated now
├── objects # Wow we have some crazy file and folder inside
│   ├── 08
│   │   └── f87015745258743015340c5466fe69c94f7587
│   ├── 10
│   │   └── ddd6d257e01349d514541981aeecea6b2e741d
│   ├── 1d
│   │   └── 12099363e995c9fc3e1d2cc68b74b8e10c361a
│   ├── info
│   └── pack
└── refs
    ├── heads
    └── tags
````

Ok, we have finished our first commit and now we have two more objects, let's check what is inside of each one:

```bash
$ git cat-file -p 1d12099363e995c9fc3e1d2cc68b74b8e10c361a
tree 08f87015745258743015340c5466fe69c94f7587
author Patrick José Pereira <myemail> 1598117804 -0300
committer Patrick José Pereira <myemail> 1598117804 -0300

First commit

$ git cat-file -p 08f87015745258743015340c5466fe69c94f7587
100644 blob 10ddd6d257e01349d514541981aeecea6b2e741d    README.md

$ git cat-file -p 10ddd6d257e01349d514541981aeecea6b2e741d
Hello!
```

As you can see, we have a commit object: **1d12099363e995c9fc3e1d2cc68b74b8e10c361a**, that points to the tree **08f87015745258743015340c5466fe69c94f7587**,
this tree has a single file on it, our old friendly **README.md**, and this same tree says that this blob has the hash **10ddd6d257e01349d514541981aeecea6b2e741d**, and this hash contains the content of **README.md**. Simple Right ?!

As I said, a tree can contain multiple blobs, or more trees, like in the following example:

{% img(url="/assets/how_to_rock/git/data-model-2.png") %}
"Git Internals Git Objects" from Git SCM is licensed under CC BY 3.0
{% end %}

And after some more commits, we end up with multiple commits, that each commit has a tree, and each tree points to more trees or more blobs!

{% img(url="/assets/how_to_rock/git/data-model-3.png") %}
"Git Internals Git Objects" from Git SCM is licensed under CC BY 3.0
{% end %}


## Wrap up git commit logic and git internals

Git, as a *simple content tracker*, uses a simple logic to manage all the files, as you saw, git works with the filesystem as a dictionary, where the filenames define the key and the content of such files are the content of this dictionary key, you can think about it as a content-addressable filesystem.

Since we have finished talking about git manages our commits, files and everything else, let us finish this deep introductory part with how the commit and the object creation works.

{% img(url="/assets/how_to_rock/git/reset-workflow.png") %}
"Reset workflow" from Git SCM is licensed under CC BY 3.0
{% end %}

The previous is a good simple example of how a commit works, first we have a untracked file in our working directory, we stage this file (`git add`) and after that we commit this file (`git commit`) the commit does update the *HEAD* (the hash where we are right now). And doing a checkout to a different hash (or *HEAD*) will result in a change of the working directory to match what was commited.

# References

Check the official Git SCM [website](https://git-scm.com/) and [repository](https://github.com/git/git-scm.com) for images and guidance.'