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

var num_goals = 7; // number of goals to show per participant

// extract batch of goals based on condition
// help from: https://github.com/jspsych/jsPsych/discussions/1705
var num_batches = 4
var goal_batch = final_stimuli[(CONDITION-1) % num_batches];

if (CONDITION % 2 == 0){
  var stimType="all-constraints"
}else{
  var stimType="single-constraint"
}

// keep track of shuffled goal order for consistency across phases
var goal_idxs = [];

var instructions = {
    type: "instructions",
    pages: ['<p> Welcome! </p> <p> We are conducting an experiment about how people come up with explanations. Your answers will be used to inform computer science and cognitive science research about explanations, causality, and language. </p>' +
            '<p> This experiment should take at most <strong>20 minutes</strong>. </br></br> You will be compensated at a base rate of $15/hour for a total of <strong>$5.00</strong>, which you will receive as long as you complete the study.</p>',
                '<p> We take your compensation and time seriously! The email for the main experimenter is <strong>katiemc@mit.edu</strong>. </br></br> Please write this down now, and email us with your Prolific ID and the subject line <i>Human experiment compensation for language experiment</i> if you have problems submitting this task, or if it takes much more time than expected. </p>',
                '<p> In this experiment, you will be reading about a causal relationship between two entitites or events. You will see text of the form: \"When X, then Y. But suppose X, and Y <strong>does not</strong> happen.\"</p>' +
                '<p> Your task is to think of and write down a possible explanation, <i>in English</i>, for how this might have occured.</p>' +
                '<p> You will see a total of <strong>' + num_goals + '</strong> scenarios. For each scenario, please write out <strong>one</strong> explanation. </p>' +
                '<p> Some scenarios may be stranger than others. There are no right answers. Please try your best regardless. </p>',
                '<p> You can write as much or as little is necessary to convey to someone how to explain the event; <strong>at most one or two sentences</strong> should be a sufficient level of detail for each scenario. </p>' +
                '<p> However, keep in mind that another human participant will be rating whether your explanations are good or bad. You will recieve a <strong>bonus</strong> for each of your explanations that gets rated as good, up to a total of <strong>$1</strong> extra.</p>',
                ],
    show_clickable_nav: true
};

var pre_check = {
    type: "instructions",
    pages: ['<p> When you are ready, please click <strong>\"Next\"</strong> to complete a quick comprehension check, before moving on to the experiment. </p>'],
    show_clickable_nav: true
};

var comprehension_check = {
   type: "survey-multi-choice",
        preamble: ["<p align='center'>Check your knowledge before you begin. If you don't know the answers, don't worry; we will show you the instructions again.</p>"],
        questions: [
            {prompt: "What will you be asked to generate?", options: ["Artistic doodle.", "Explanations for events.", "Poems.",], required: true},
            {prompt: "How will you be providing your answer?", options: ["By writing text.", "By drawing pictures.", "Filling out a multiple choice questionnaire."], required: true},
            {prompt: "We will be checking your answers to ensure they can be used for academic research. Which of the following could impact your payment for this task?",
            options: ["Not making a good attempt to write a high-quality answer for each task.",
            "Writing creative but unusual answers for each task.",
            "Writing high-quality but risky answers for each task."], required: true},
        ],
            on_finish: function(data) {
              var responses = data.response;

              if (responses['Q0'] == "Explanations for events." && responses['Q1'] == "By writing text." && responses['Q2']=="Not making a good attempt to write a high-quality answer for each task.") {
                familiarization_check_correct = true;
              }else{
                familiarization_check_correct=false;
              }
            }
}

var familiarization_timeline = [instructions, quality_control, pre_check, comprehension_check]

var familiarization_loop = {
              timeline: familiarization_timeline,
              loop_function: function(data) {
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

var parse_goal_and_constraint = function parse_goal_and_constraint(goal, constraints){
  // if constraints is not empty, concatenate to goal
  // move end-of-sentence to end of constraint
  // for now, only use one constraint

  if (constraints == ""){
    return goal
  } else{
    constraint =  constraints.split(';')[0]
    return goal.slice(0, -1) + ' <i>' + constraint + '</i>.'
  }

}

var generate_text = {
    type: 'survey-text',
    questions: [
        {prompt: function() {
          var scenario = jsPsych.timelineVariable('scenario')

          var constraint = jsPsych.timelineVariable(stimType) + "."

          console.log(stimType)

          var ifClause = scenario.split('.')[0] + '.'
          var event = scenario.split('.')[1] + '.'

          if (stimType == "all-constraints"){
            var constraintStr = "Write an answer that does <strong>NOT</strong> use any of the following: " + constraint
          }else{
            var constraintStr = "Write an answer that does <strong>NOT</strong> include that " + constraint
          }

          var display_str = "<p>"+ ifClause + "</p><p>" + event + "</p><p>" + constraintStr +
          "</p>Answer as if you are <strong>continuing the sentence</strong> \"<strong>Why? This could have happened because...</strong>"

          return display_str

        },
          rows: 5, columns: 50,
          required: true,
          placeholder: '...complete the sentence with your explanation here! 1 or 2 sentences should be enough.',
          name: "Explanation"
        },
    ],
    data: {
        prompt: jsPsych.timelineVariable('scenario'),
        task: 'generate, ' + stimType,
        constraint: jsPsych.timelineVariable(stimType)
    },
    on_finish: function() {
      var curr_progress_bar_value = jsPsych.getProgressBarCompleted();
      var prop_increase = 1/(num_goals * 2); // because 2 phase
      jsPsych.setProgressBar(curr_progress_bar_value + prop_increase);
    }
};


var generate_task = {
    timeline: [generate_text],
    timeline_variables: goal_batch,
    data: {
        phase: 'test'
    },

    sample: {
        type: 'custom',
          fn: function(t) {
          // t = set of indices from 0 to n-1, where n = # of trials in stimuli variable
           // returns a set of indices for trial

          // shuffle the current batch of goals
          // save order to be used again for Phase 2
          // shuffle and save that set and for use in Phase 2
          goal_idxs = jsPsych.randomization.shuffle(t)
          return goal_idxs

        }

    }
}
timeline.push(generate_task);


var comments_block = {
    type: "survey-text",
    preamble: "<p>Thank you for participating in our study!</p>"+
    "<p>Click <strong>\"Finish\"</strong> to complete the experiment and receive compensation. If you have any comments about Phase 1 and/or Phase 2, please let us know in the form below.</p>",
    questions: [
      {prompt: "Were the instructions clear? (On a scale of 1-10, with 10 being very clear)"},
      {prompt: "How challenging was Phase 1 of the experiment? (On a scale of 1-10, with 10 being very challenging)"},
      {prompt: "How engaging was Phase 1 of the experiment? (On a scale of 1-10, with 10 being very engaging)"},
      {prompt: "Do you have any additional comments to share with us?",rows: 5, columns: 50}],
    button_label: "Finish",
};
timeline.push(comments_block)


jsPsych.init({
    timeline: timeline,
    on_finish: function () {
        // send back to main prolific link
        window.location = "https://app.prolific.co/submissions/complete?cc=4E967F29"
    },
    show_progress_bar: true,
    auto_update_progress_bar: false
});
