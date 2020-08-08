+++
title = 'How to rock: First tips'
date = 2020-08-08T08:28:00z
[taxonomies]
tags = [ "kde", "development", "tutorial", "how-to-rock" ]
[extra]
header = "/assets/how_to_rock/banner.jpeg"
+++

After working for some time collaborating with open source/free software projects, I started to help newcomers to contribute and push the development further with good practices. The following post will try to itemize some important tips that can be used for software collaboration and personal projects.


<!-- more -->

# Code practices

- **Encapsulate magic variables**:
  ```cpp
  ...// First version
    start_communication(0, 1, 232);
    // Reviewer: What is the meaning of 0 ? What is 1 ? Why 232 ?

  ...// Second version
    enum class Messages {
        ...
        RequestStatus = 232,
    }
    ...
    const uint8_t vid = 0;
    const uint8_t cid = 1;
    start_communication(vid, cid, Messages::RequestStatus);
    // Reviewer: What is vid ? What is cid ?

  ...//Final version
    ...
    const uint8_t vehicle_id = 0;
    const uint8_t component_id = 1;
    start_communication(vehicle_id, component_id, Messages::RequestStatus);
  ```
  As you can see, the final version makes everything more readable, we know that we are starting the communication with a vehicle that has an id of 0 and the vehicle probably contains a component with id 1, and while calling this function we are also requesting the status. Much better than 0, 1 and 232 right ?
  Doing this will help the reviewers and future developers to understand what is the meaning of such numbers.
  It's also necessary to avoid variables that contains only single letters or really short abbreviations, is much harder to understand this: $$C^2 = A^2 + B^2$$
  over this: $$hypotenuse^2 = catheti_1^2 + catheti_2^2$$

- **Avoid multiple arguments**:
    ```cpp
    ...// First version
    auto vehicle = new Vehicle(
        VehicleType::Car,
        4,
        {28, 31},
        Fuel::Electric,
        1.2,
        613
    );
    // Reviewer: What is the meaning of all this values ?
    //           How can we make it better ?

    ...// Second version
    auto vehicle = new Vehicle(VehicleType::Car)
    vehicle->setNumberOfTires(4);
    vehicle->setTirePressure({28, 31});
    vehicle->setFuel(Fuel::Electric);
    vehicle->setWeightInTons(1.2);
    vehicle->setAutonomyInKm(613);

    ...// It's also possible to use aggregate initialization in C++20
    // and user-defined literals from C++11
    auto vehicle = new Vehicle({
        .type = VehicleType::Car,
        .numberOfTires = 4,
        .tirePressure = {28_psi, 31_psi},
        .fuel = Fuel::Electric,
        .weight = 1.2_tn,
        .autonomy = 613_km,
    });
    ```

    Both second and C++20/C++11 alternatives are valid for a better readability of the code, to choose between both alternatives will depend of how are you going to design your API, probably if you are more familiar with the Qt API, the second version appears to be the most common, the C++20/C++11 alternative appears to be a bit more verbose but can be useful to avoid multiple function calls and helpful when dealing with a simpler code base.

- **Encapsulate code when necessary**, try to break functions in a more readable and explanatory way:
    ```cpp
    ...// Original version
    void Serial::start_serial_communication() {
        // Check if we are open to talk
        if (!_port || _port->register() != 0xb0001) {
            log("Serial port is not open!");
            return false;
        }

        // Send a 10ms serial break signal
        _port->set_break_enabled(true);
        msleep(10);
        _port->set_break_enabled(false);
        usleep(10);
        // Send intercalated binary for detection
        _port->write('U');
        _port->flush();

        // Send start AT command
        _port->write("AT+start");
    }

    // Reviewer: Try to make it more readable encapsulating
    //            some functionalities

    ...// Second version
    bool Serial::is_port_open() {
        return !_port || _port->register() != 0xb0001;
    }

    void Serial::force_baudrate_detection() {
        // Send a 10ms serial break signal
        _port->set_break_enabled(true);
        msleep(10);
        _port->set_break_enabled(false);
        usleep(10);
        // Send intercalated binary for detection
        _port->write('U');
        _port->flush();
    }

    void Serial::send_message(Message message_type) {
        _port->write(messageFromType(message_type));
    }

    void Serial::start_serial_communication() {
        if (!is_port_open()) {
            log("Serial port is not open!");
            return false;
        }

        force_baudrate_detection();
        send_message(Message::Start)
    }
    ```
    As you can see, the reason behind each block of code is clear now, and with that, the comments are also not necessary anymore, the code is friendly and readable enough that's possible to understand it without any comments, the function name does the job for free.

- **Avoid comments**, that's a clickbait, comments are really necessary, but they may be unnecessary when you are doing something that's really obvious, and sometimes when something is not obvious, it's better to encapsulate it.
    ```cpp
        ...// Original version
        void blink_routine() {
            // Use the LED builtin
            const int led_builtin = LED_BUILTIN;
            // Configure ping to output
            setPinAsOutput(led_builtin);

            // Loop forever
            while(true) {
                // Turn the LED on
                turnPinOn(led_builtin);
                // Wait for a second
                wait_seconds(1);
                // Turn the LED off
                turnPinOff(led_builtin);
                // Wait for a second
                wait_seconds(1);
            }
        }
    ```
    Before checking the final version, let me talk more about it:

    - For each line of code you'll have a comment (like a parrot that repeat what we say), and the worst thing about these comments is that the content is exactly what you can read from the code! You can think that this kind of comment is dead code, something that has the same meaning as the code, but it does not run, resulting in a duplicated amount of lines to maintain. If you forget to update each comment for each line of code, you'll have a comment that does not match with the code, and this will be pretty confuse for someone that's reading it.

    - **One of the most important skills about writing comments, is to know when not to write it!**

    - A comment should bring a value to the code, if you can remove the comment and the code can be understandable by a newcomer, the comment is not important.

    ```cpp
    ...// Final version
        void blink_routine() {
            const int led_builtin = LED_BUILTIN;
            setPinAsOutput(led_builtin);

            while(true) {
                turnPinOn(led_builtin);
                wait_seconds(1);
                turnPinOff(led_builtin);
                wait_seconds(1);
            }
        }
    ```

    There is a good video about this subject by [Walter E. Brown in cppcon 2017, "Whitespace ≤ Comments ＜＜ Code"](https://www.youtube.com/watch?v=NLebZ3XT92E).

    And to finish, you should not avoid comments, you should understand when comments are necessary, like this:
    ```cpp
    // From ArduPilot - GPIO_RPI
    void set_gpio_mode_alt(int pin, int alternative) {
        // **Moved content from cpp for this example**
        const uint8_t pins_per_register = 10;
        // Calculates the position of the 3 bit mask in the 32 bits register
        const uint8_t tree_bits_position_in_register = (pin%pins_per_register)*3;
        /** Creates a mask to enable the alternative function based in the following logic:
        *
        * | Alternative Function | 3 bits value |
        * |:--------------------:|:------------:|
        * |      Function 0      |     0b100    |
        * |      Function 1      |     0b101    |
        * |      Function 2      |     0b110    |
        * |      Function 3      |     0b111    |
        * |      Function 4      |     0b011    |
        * |      Function 5      |     0b010    |
        */
        const uint8_t alternative_value =
            (alternative < 4 ? (alternative + 4) : (alternative == 4 ? 3 : 2));
        // 0b00'000'000'000'000'000'000'ALT'000'000'000 enables alternative for the 4th pin
        const uint32_t mask_with_alt = static_cast<uint32_t>(alternative_value) << tree_bits_position_in_register;
        const uint32_t mask = 0b111 << tree_bits_position_in_register;
        // Clear all bits in our position and apply our mask with alt values
        uint32_t register_value = _gpio[pin / pins_per_register];
        register_value &= ~mask;
        _gpio[pin / pins_per_register] = register_value | mask_with_alt;
    }
    ```
    Mostly of the lines in this code can be impossible to understand without access or reading the datasheet directly,
    the comments are here to understand what is going on and why, otherwise anyone that'll touch this code will need to do a reverse engineer to understand it.

# Development flow

- **Avoid creating multiple Pull Requests (PRs)**, update the ones that are still open.
  - E.g: You created a Pull Request called "Add button feature", some modifications will be necessary after the review process, and for that you'll need to update the same branch over creating new ones. That's necessary to help the project maintainers to see previous comments and the development history. Creating multiple PRs will only make the maintainers confuse and unable to track old comments, suggestions and your code changes between PRs.

- **Create atomic and self-contained commits**, avoid doing multiple tasks in the same commit.
  - E.g: You created a commit to fix the serial communication class, and inside the same commit you are doing 3 different tasks, removing trailing spaces, fixing a pointer validation check and a typo in the documentation of a different class. This appear to be silly and bureaucratic, but there are good reasons to break this simple commit and at least 3 different commits, one for the pointer check, a second one for the typo and a third one for the trailing space.

    Developers usually track lines history to understand the changes behind a functionality, it's common to search with grep history from commits or line changes in specific commits to understand the history of a library, function, class, or a small feature, if the commits start to be polluted with unnecessary changes, this development practice will be almost impossible to be done, since a bunch of unrelated lines will me changed between commits and this technic will be unable to help the dear developer. `git blame` will also be of little help.

    The example was also really simple, but you can imagine what happens if you change different parts of the code, for unrelated things, and a bug appears, technics such as `git bisect` will still work, but the result will be much harder to understand and to find which line is the one that created such bug.

- **Create atomic and self-sustained PRs**, avoid doing multiple things in the same PR, like different features. They may appear simple with small pieces of code/functionality but they can escalate quickly after a review process, and if both features are somehow related or dependently, it's recommended to break it in multiple PRs with code to maintain compatibility with current code base.
  - E.g: You have applied a PR for software notifications, and somehow you also added a URL fetch functionality to grab new software versions from the server. After the first review, the maintainer asks to create a more abstracted way to fetch data from a REST API and to deal with network requirements, this will start to convolute the PR, moving the initial idea of the notification feature to an entire network REST API architecture. With that, it's better to break the PR in two, one that only provides the notification and a second PR that is used for the REST API related code.

- **Do your own review**, the final and probably most important tip of all, doing that will train your mind and eyes to detect poor code standards or bad practices, it'll also make your PR be merged easily and faster, since you'll be able to catch problems before the reviewer feedback. Some reviewers may think that reviewing your own PR is a must, since we are talking about open source projects and free software, you should understand that the people that are reviewing your code are not obligated to do so, the majority are collaborating and donating their own time to help the development and maintenance of such projects, doing your own review is a sign of empathy about the project and maintainer time.


# Final comment

This is the first post of a series that I'm planning to do. Hope that some of these points may help you in your journey.

## References
- [CppCon 2019: Kate Gregory “Naming is Hard: Let's Do Better”](https://www.youtube.com/watch?v=MBRoCdtZOYg)
- [CppCon 2018: Kate Gregory “Simplicity: Not Just For Beginners”](https://www.youtube.com/watch?v=n0Ak6xtVXno)
- [CppCon 2018: Kate Gregory “What Do We Mean When We Say Nothing At All?”](https://www.youtube.com/watch?v=kYVxGyido9g)
- [CppCon 2017: Lars Knoll “Qt as a C++ Framework: History, Present State and Future”](https://www.youtube.com/watch?v=YWiAUUblD34)
- [CppCon 2017: Kate Gregory “10 Core Guidelines You Need to Start Using Now”](https://www.youtube.com/watch?v=XkDEzfpdcSg)
- [API Design Principles - TQtC](https://wiki.qt.io/API_Design_Principles)
- [Designing Qt-Style C++ APIs - Matthias Ettrich](https://doc.qt.io/archives/qq/qq13-apis.html)
- [The Little Manual of API Design - Jasmin Blanchette](https://people.mpi-inf.mpg.de/~jblanche/api-design.pdf)
