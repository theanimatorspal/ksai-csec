// Java.perform(() => {
//     let ExampleClass = Java.use("io.hextree.fridatarget.ExampleClass");
//     let ExampleInstance = ExampleClass.$new();
//     console.log(ExampleInstance.returnDecryptedString());
//     console.log(ExampleInstance.returnDecryptedStringIfPasswordCorrect("VerySecret"));
// });

// Java.perform(() => {
//     let FlagClass = Java.use("io.hextree.fridatarget.FlagClass");
//     let FlagInstance = FlagClass.$new()
//     console.log(FlagInstance.flagFromInstanceMethod());
//     console.log(FlagInstance.flagIfYouCallMeWithSesame("sesame"));
// })

// Java.perform(() => {
//     // let ActivityClass = Java.use("android.app.Activity");
//     // ActivityClass.onResume.implementation = function() {
//     //     console.log("Activity Resumed", this.getClass().getName());
//     //     this.onResume();
//     // }
//     let FragmentClass = Java.use("androidx.fragment.app.Fragment")
//     FragmentClass.onResume.implementation = function() {
//         console.log("Fragment Resumed", this.getClass().getName());
//         this.onResume();
//     }
// });

Java.perform(() => {
    let DiceGameFragment = Java.use("io.hextree.fridatarget.ui.DiceGameFragment");
    DiceGameFragment["randomDice"].implementation = function () {
        console.log(`DiceGameFragment.randomDice is called`);
        let result = this["randomDice"]();
        console.log(`DiceGameFragment.randomDice result=${result}`);
        return 5;
    };
});