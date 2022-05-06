var timeline = []

// capture info from Prolific
// help from: https://www.jspsych.org/overview/prolific/
var subject_id = jsPsych.data.getURLVariable('PROLIFIC_PID');
var study_id = jsPsych.data.getURLVariable('STUDY_ID');
var session_id = jsPsych.data.getURLVariable('SESSION_ID');

jsPsych.data.addProperties({
    subject_id: subject_id,
    study_id: study_id,
    session_id: session_id
});

var items_in_batch = []
var goals_in_batch = []
for (var i = 0; i < all_generations.length; i++){
  if (all_generations[i]["cond_idx"] == condition_num){
    items_in_batch.push(all_generations[i])
    goals_in_batch.push(all_generations[i]["goal"])
  }
}
var sampled_goals = Array.from(new Set(goals_in_batch))
sampled_goals = jsPsych.randomization.shuffle(sampled_goals)
var num_goals = sampled_goals.length

// separate out so explanations (or plans) for each stimuli are indexable
var batch_goal_plans = []
for (var j = 0; j < num_goals; j++){
    var current_goal = sampled_goals[j]
    console.log(current_goal)
    var generated_plans = []
    console.log(generated_plans)
    for (var i = 0; i < items_in_batch.length; i++){
        console.log(i)
        if (current_goal == items_in_batch[i]["goal"]) {
            generated_plans.push(items_in_batch[i])
        }
    }
    console.log(generated_plans)
    batch_goal_plans.push(generated_plans)
}

var num_goal_types = 3
console.log(batch_goal_plans)
var num_plans = batch_goal_plans[0].length; // should be equal len b/w A and B

console.log(num_plans)

var progress_bar_increase = 1 / (num_plans * num_goal_types)

console.log(progress_bar_increase)

var overall_goodness_scale = [
    "The worst",
    "Very bad",
    "Somewhat bad",
    "Neutral",
    "Somewhat good",
    "Very good",
    "The best"
]

var instructions = {
    type: "instructions",
    pages: ['<p> Welcome! </p> <p> We are conducting an experiment about how people come up with explanations. Your answers will be used to inform computer science and cognitive science research about explanations, causality, and language. You can receive up to <strong>$0.50</strong> bonus if it is clear you try your best at our task.</p>' +
    '<p> This experiment should take at most <strong>20 minutes</strong>. </br></br> You will be compensated at a base rate of $13.50/hour for a total of <strong>$4.50</strong>, which you will receive as long as you complete the study.</p>',
        '<p> We take your compensation and time seriously! The email for the main experimenter is <strong>katiemc@mit.edu</strong>. </br></br> Please write this down now, and email us with your Prolific ID and the subject line <i>Human experiment compensation for language experiment</i> if you have problems submitting this task, or if it takes much more time than expected. </p>',
         '<p> Note that this experiment will also involve unfiltered text. As such, some text may contain sensitive and/or explicit content. If you are uncomfortable at any time, you are always free to stop and exit the study. If you notice any harmful or disconcerting language, please contact the experimenter (at <strong>katiemc@mit.edu</strong>).</p>',
        '<p>In this experiment, you will be reading a series of <strong>causal relationships</strong> between two entitites or events (like \"When a carpet gets wet, then mold grows. But suppose a carpet gets wet, but then mold does not grow.\"), and <strong>explanations</strong> written in English for why that scenario could have happened (e.g., \"This could have happened because the carpet was covered in anti-mold film.\").</p>'+
        '<p> Your task will be to <strong>rate how good each explanation is</strong> for explaining how a scenario could have occured.</p>'+
        '<p> You can interpret "good" however makes sense to you. </p>' +
        '<p>You will enter your answer for each question by clicking a rating on a <strong>7-point multiple choice scale</strong> ranging from <strong>1 (worst)</strong> to <strong>7 (best)</strong>.',

        '<p>You will see explanations for <strong>3 different scenarios</strong>.</p>' +
        '<p>There will be a total of <strong>20 explanations</strong> for you to rate per scenario.</p>' +
        '<p>You will get a <strong>15 second break</strong> in between scenarios.</p>',


        '<p> When you are ready, please click <strong>\"Next\"</strong> to complete a quick comprehension check, before moving on to the experiment. </p>'],
    show_clickable_nav: true
};

var comprehension_check = {
    type: "survey-multi-choice",
    preamble: ["<p align='center'>Check your knowledge before you begin. If you don't know the answers, don't worry; we will show you the instructions again.</p>"],
    questions: [
        {
            prompt: "What will you be asked to rate in this task?",
            options: ["The goodness of explanations.", "The creativity of drawings.", "The funniness of jokes.",],
            required: true
        },
        {
            prompt: "How will you be providing your answer?</i>",
            options: ["By writing text.", "By selecting an option from a multiple choice scale.", "By moving a slider."],
            required: true
        },
    ],
    on_finish: function (data) {
        var responses = data.response;

        if (responses['Q0'] == "The goodness of explanations." && responses['Q1'] == "By selecting an option from a multiple choice scale.") {
            familiarization_check_correct = true;
        } else {
            familiarization_check_correct = false;
        }
    }
}

var familiarization_timeline = [instructions, comprehension_check]

var familiarization_loop = {
    timeline: familiarization_timeline,
    loop_function: function (data) {
        return !familiarization_check_correct;
    }
}

timeline.push(familiarization_loop)

var final_instructions = {
    type: "instructions",
    pages: ['<p> Now you are ready to begin! </p>' +
    '<p> Please click <strong>\"Next\"</strong> to start the experiment. Thank you for participating in our study! </p>'],
    show_clickable_nav: true
};
timeline.push(final_instructions)

function correct_capitalization(string) {
  // help from: https://www.codegrepper.com/code-examples/javascript/how+to+make+first+word+capital+of+each+sentence+in+a+paragraph+javascript
	var new_str = ""
	var inidices_to_capitalize = new Set([0]) // always include the first index

	// any any periods (starting from after next space)
	for(var i=1; i<string.length;i++) {
    if (string[i] === ".") {
      if (i != (string.length-1) & string[i+1] == " "){
      inidices_to_capitalize.add(i+2)
		  }
    }; // start from after space
  }

	for(var i = 0; i<string.length;i++){
		if (inidices_to_capitalize.has(i)){
			new_str += string[i].toUpperCase()
		} else{
			new_str += string[i]
		}
	}
    return new_str;
}


for (var i = 0; i < batch_goal_plans.length; i++){
var generated_plans = batch_goal_plans[i]
var rating_page = {
    type: 'survey-likert',
    questions: [
        {
            prompt: function () {
                // var goal = jsPsych.timelineVariable('goal').slice(5)

                var scenario = jsPsych.timelineVariable('goal').slice(10)

                var ifClause = scenario.split('.')[0] + '.'
                var event = scenario.split('.')[1] + '.'

                // ensure that text after a period start capitalized
                // correction for human plans so it stylistically matches
                var plan = correct_capitalization(jsPsych.timelineVariable('plan').replace(/\n/g, "<br />"))

                return "<p><strong>Scenario: </strong>"+ scenario + "</p>"
                    // + '<p><strong>Plan: </strong>' + jsPsych.timelineVariable('plan').replace(/\n/g, "<br />") +
                   + '<p><strong>Explanation: </strong>' + plan +

                    '</p><p></p>' +
                    '<br></br><p>' +
                    '<strong>How good is this explanation overall? Assign it a single score that summarizes how good it is for this scenario.</strong></p>' //+
            },
            name: "goodness", labels: overall_goodness_scale, required: true,
        }
    ],
    randomize_question_order: false,
};

var rating_task = {
    timeline: [rating_page],
    timeline_variables: generated_plans,
    data: {
        prompt: jsPsych.timelineVariable('goal'),
        task: 'rate_goodness',
        subj_id: jsPsych.timelineVariable('id'),
        plan: jsPsych.timelineVariable('plan'),
        goal_type: jsPsych.timelineVariable('goal_type'),
    },
    sample: {
        type: 'custom',
        fn: function (t) {
            // t = set of indices from 0 to n-1, where n = # of trials in stimuli variable
            // returns a set of indices for trials
            return jsPsych.randomization.shuffle(t)
        }
    },
    on_finish: function () {
        var curr_progress_bar_value = jsPsych.getProgressBarCompleted();
        jsPsych.setProgressBar(curr_progress_bar_value + progress_bar_increase);
    }
}

timeline.push(rating_task);

var block_pause = {
    type: "html-keyboard-response",
    choices: jsPsych.NO_KEYS,
    stimulus: "<p><b>Break</b></p>" +
    "<p>You will now get a 15 second break before moving on to the next scenario. The screen will automatically disappear when the time is up. After which, please continue with the task.</p>",
    trial_duration: 15000
    };

if (i != (batch_goal_plans.length-1)){
 // no need for a pause between for the final goal
    timeline.push(block_pause)

}
}

var comments_block = {
    type: "survey-text",
    preamble: "<p>Thank you for participating in our study!</p>" +
    "<p>Click <strong>\"Finish\"</strong> to complete the experiment and receive compensation. If you have any comments about the experiment, please let us know in the form below.</p>",
    questions: [
        {prompt: "Were the instructions clear? (On a scale of 1-10, with 10 being very clear)"},
        {prompt: "How challenging was it to come up with a rating per explanation? (On a scale of 1-10, with 10 being very challenging)"},
        {prompt: "Were there any particular qualities of explanations you looked to when deciding if a explanation was good?", rows:5,columns:50},
        {prompt: "Do you have any additional comments to share with us?", rows: 5, columns: 50}],
    button_label: "Finish",
};
timeline.push(comments_block)

jsPsych.init({
    timeline: timeline,
    on_finish: function () {
        // send back to main prolific link
        // window.location = "https://www.google.com/"
        window.location = "https://app.prolific.co/submissions/complete?cc=69A40EE2"
    },
    show_progress_bar: true,
    auto_update_progress_bar: false
});
