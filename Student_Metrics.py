# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
from datetime import datetime, date
import hmac
import altair as alt

st.set_page_config(page_title='Institution TJ Scholar Dashboard',layout='wide')

# Add CSS styling for right alignment of all table data
st.markdown("""
<style>
    /* Right align all table data */
    .dataframe {
        text-align: right !important;
    }
    
    .dataframe th {
        text-align: right !important;
    }
    
    .dataframe td {
        text-align: right !important;
    }
    
    /* Ensure Streamlit tables are right aligned */
    div[data-testid="stDataFrame"] {
        text-align: right !important;
    }
    
    div[data-testid="stDataFrame"] table {
        text-align: right !important;
    }
    
    div[data-testid="stDataFrame"] th {
        text-align: right !important;
    }
    
    div[data-testid="stDataFrame"] td {
        text-align: right !important;
    }
    
    /* Additional targeting for all table elements */
    table {
        text-align: right !important;
    }
    
    table th {
        text-align: right !important;
    }
    
    table td {
        text-align: right !important;
    }
    
    /* Target specific Streamlit components */
    .stDataFrame {
        text-align: right !important;
    }
    
    .stDataFrame table {
        text-align: right !important;
    }
    
    .stDataFrame th {
        text-align: right !important;
    }
    
    .stDataFrame td {
        text-align: right !important;
    }
    
    /* Force alignment on all table cells */
    td, th {
        text-align: right !important;
    }
</style>
""", unsafe_allow_html=True)

st.title('Institution TJ - Scholar Dashboard')

# Password protection
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

## Read data from CSV files
df_engagement_attendance = pd.read_csv('./student-data/institution-1-engagement-data.csv',parse_dates=['start_date','end_date'])
df_test_scores = pd.read_csv('./student-data/institution-1-test-data.csv',parse_dates=['test_date'])
df_test_section_scores = pd.read_csv('./student-data/institution-1-2025-exam-data-jw-exams.csv')
df_tier_data = pd.read_csv('./student-data/tierdata.csv')
df_retakers = pd.read_csv('./student-data/retakers_data_ey24.csv')

## Create dashboard filters
student_id = st.selectbox("Choose a student:", list(df_engagement_attendance['student_id'].unique()))
st.write('Here is a link to the [Texas JAMP Scholar Student Roster with Associated Student ID Numbers](https://drive.google.com/file/d/1HxzBblcUgBndh-61grpsCwsSv2JSJmXx/view?usp=sharing)')

## Transform dataframes
df_engagement_attendance_student_filtered = df_engagement_attendance[df_engagement_attendance['student_id'] == student_id]
# Create date_range column for tooltips
df_engagement_attendance_student_filtered['date_range'] = df_engagement_attendance_student_filtered.apply(
    lambda row: f"{row['start_date'].strftime('%m/%d/%y')} - {row['end_date'].strftime('%m/%d/%y')}", 
    axis=1
)
df_engagement_attendance_student_filtered['num_attended_large_session_cumsum'] = df_engagement_attendance_student_filtered['num_attended_large_session'].cumsum()
df_engagement_attendance_student_filtered['num_scheduled_large_session_cumsum'] = df_engagement_attendance_student_filtered['num_scheduled_large_session'].cumsum()
df_engagement_attendance_student_filtered['num_attended_small_session_cumsum'] = df_engagement_attendance_student_filtered['num_attended_small_session'].cumsum()
df_engagement_attendance_student_filtered['num_scheduled_small_session_cumsum'] = df_engagement_attendance_student_filtered['num_scheduled_small_session'].cumsum()
df_engagement_attendance_student_filtered['large_session'] = df_engagement_attendance_student_filtered['num_attended_large_session_cumsum'] / df_engagement_attendance_student_filtered['num_scheduled_large_session_cumsum']
df_engagement_attendance_student_filtered['small_session'] = df_engagement_attendance_student_filtered['num_attended_small_session_cumsum'] / df_engagement_attendance_student_filtered['num_scheduled_small_session_cumsum']
df_engagement_attendance_avg = df_engagement_attendance_student_filtered[['class_participation','homework_participation','cars_accuracy','sciences_accuracy','class_accuracy']].mean()

class_participation = df_engagement_attendance_avg.loc['class_participation']
homework_participation = df_engagement_attendance_avg.loc['homework_participation']
overall_participation = (class_participation + homework_participation) / 2

df_test_scores['test_date'] = df_test_scores['test_date'].dt.date
df_test_scores_student_filtered = df_test_scores[df_test_scores['student_id'] == student_id]

df_test_section_scores_student_filtered = df_test_section_scores[df_test_section_scores['student_id'] == student_id]
df_tier_data_student_filtered = df_tier_data[df_tier_data['student_id'] == student_id]

## Create sections and render dashboard
st.write(' ')
st.write(' ')

# Add CSS styling for larger tabs
st.markdown("""
<style>
    /* Make tabs larger and more appealing */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding-left: 1rem;
        padding-right: 1rem;
        font-size: 1.2rem;
        font-weight: 600;
        color: #2c3e50;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #e3f2fd;
        border-bottom: 3px solid #2196f3;
        color: #1976d2;
        font-weight: 700;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f5f5f5;
        color: #1976d2;
        transform: translateY(-1px);
    }
    
    .stTabs [data-baseweb="tab"]:not([aria-selected="true"]):hover {
        background-color: #f8f9fa;
        color: #1976d2;
    }
</style>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2 = st.tabs(["Individual Student Metrics", "Retaker Cohort"])

with tab1:
    # Student Tier Assessment - moved to very top
    st.header('Student Tier Assessment')
    st.caption('The tiers listed below represent student data gathered throughout their time in our MCAT program, from June 2024 to now.')
    st.write(' ')

    # Check if we have tier data for this student
    if not df_tier_data_student_filtered.empty:
        # Create a container for consistent width
        with st.container():
            # Create a more user-friendly display of tier data
            tier_display = pd.DataFrame({
                'Assessment Category': ['Survey Completion', 'Class Attendance', 'Small Group Attendance', 'Class Participation', 'Overall Assessment'],
                'Performance Tier': [
                    df_tier_data_student_filtered['Survey Tier'].values[0],
                    df_tier_data_student_filtered['Large Group Tier'].values[0],
                    df_tier_data_student_filtered['Small Group Tier'].values[0],
                    df_tier_data_student_filtered['Class Participation Tier'].values[0],
                    df_tier_data_student_filtered['Final Tier'].values[0]
                ]
            })
            
            # Display the tier information in a table
            # st.dataframe(tier_display, use_container_width=True)
            
            # Optional: Add a visual representation of the tiers using colored indicators
            col1, col2, col3, col4, col5 = st.columns(5)
            
            # Helper function to display tier with appropriate color
            def display_tier(column, category, tier):
                colors = {
                    'Tier 1': '#1B5E20',  # Dark green
                    'Tier 2': '#FF9800',  # Light orange
                    'Tier 3': '#EF5350',  # Red
                    'Tier 4': '#EF5350'   # Red
                }
                color = colors.get(tier, '#9E9E9E')  # Default to grey if tier not recognized
                column.markdown(f"<h5 style='text-align: center'>{category}</h5>", unsafe_allow_html=True)
                column.markdown(f"<div style='background-color: {color}; padding: 10px; border-radius: 5px; text-align: center; color: white; font-weight: bold;'>{tier}</div>", unsafe_allow_html=True)
            
            # Display each category with its tier
            display_tier(col1, 'Survey Completion', df_tier_data_student_filtered['Survey Tier'].values[0])
            display_tier(col2, 'Class Attendance', df_tier_data_student_filtered['Large Group Tier'].values[0])
            display_tier(col3, 'Small Group Attendance', df_tier_data_student_filtered['Small Group Tier'].values[0])
            display_tier(col4, 'Class Participation', df_tier_data_student_filtered['Class Participation Tier'].values[0])
            display_tier(col5, 'Overall', df_tier_data_student_filtered['Final Tier'].values[0])
    else:
        st.info("No tier assessment data available for this student.")

    st.write(' ')
    st.write(' ')

    # Summer Student Tier Assessment
    st.header('Summer Student Tier Assessment')
    st.caption('The tiers listed below represent student data gathered during the summer 2025 program.')
    st.write(' ')

    # Check if we have summer tier data for this student
    df_retakers_student_filtered = df_retakers[df_retakers['student_id'] == student_id]
    if not df_retakers_student_filtered.empty:
        # Create a container for consistent width
        with st.container():
            # Create a more user-friendly display of summer tier data
            summer_tier_display = pd.DataFrame({
                'Assessment Category': ['Survey Completion', 'Class Attendance', 'Small Group Attendance', 'Class Participation'],
                'Performance Tier': [
                    df_retakers_student_filtered['Summer_SurveyTier'].values[0],
                    df_retakers_student_filtered['Summer _Large Group Attendance Tier'].values[0],
                    df_retakers_student_filtered['Summer_ Small_Group_Attendance_Tier'].values[0],
                    df_retakers_student_filtered['Summer_ClassParticipation_Tier'].values[0]
                ]
            })
            
            # Optional: Add a visual representation of the summer tiers using colored indicators
            col1, col2, col3, col4 = st.columns(4)
            
            # Helper function to display tier with appropriate color
            def display_summer_tier(column, category, tier):
                colors = {
                    'Tier 1': '#1B5E20',  # Dark green
                    'Tier 2': '#FF9800',  # Light orange
                    'Tier 3': '#EF5350',  # Red
                    'Tier 4': '#EF5350'   # Red
                }
                color = colors.get(tier, '#9E9E9E')  # Default to grey if tier not recognized
                column.markdown(f"<h5 style='text-align: center'>{category}</h5>", unsafe_allow_html=True)
                column.markdown(f"<div style='background-color: {color}; padding: 10px; border-radius: 5px; text-align: center; color: white; font-weight: bold;'>{tier}</div>", unsafe_allow_html=True)
            
            # Display each category with its summer tier
            display_summer_tier(col1, 'Survey Completion', df_retakers_student_filtered['Summer_SurveyTier'].values[0])
            display_summer_tier(col2, 'Class Attendance', df_retakers_student_filtered['Summer _Large Group Attendance Tier'].values[0])
            display_summer_tier(col3, 'Small Group Attendance', df_retakers_student_filtered['Summer_ Small_Group_Attendance_Tier'].values[0])
            display_summer_tier(col4, 'Class Participation', df_retakers_student_filtered['Summer_ClassParticipation_Tier'].values[0])
    else:
        st.info("No summer tier assessment data available for this student.")

    st.write(' ')
    st.write(' ')

    # Tier Criteria Legend
    st.header('Tier Criteria Legend')
    st.caption('The criteria below represent the thresholds used to determine student tiers based on their performance across different engagement metrics.')
    st.write(' ')

    # Add CSS styling for the tier criteria legend
    st.markdown("""
    <style>
    .tier-flex {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        width: 100%;
    }
    .tier-column {
        width: 32%;
    }
    .tier1-text {
        color: #4CAF50;
        font-weight: bold;
    }
    .tier2-text {
        color: #FF9800;
        font-weight: bold;
    }
    .tier3-text {
        color: #EF5350;
        font-weight: bold;
    }
    .tier-criteria {
        margin: 6px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Then create each column separately
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <p class="tier1-text">Tier 1 Students</p>
        <div class="tier-criteria" style="color: #4CAF50;">Responsiveness to Surveys (≥90%)</div>
        <div class="tier-criteria" style="color: #4CAF50;">Attendance in Sessions (≥80%)</div>
        <div class="tier-criteria" style="color: #4CAF50;">Participation (≥75%)</div>
        <div class="tier-criteria" style="color: #4CAF50;">Engagement (≥75%)</div> 
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <p class="tier2-text">Tier 2 Students</p>
        <div class="tier-criteria" style="color: #FF9800;">Responsiveness to Surveys (50% - 89%)</div>
        <div class="tier-criteria" style="color: #FF9800;">Attendance in Sessions (50% - 79%)</div>
        <div class="tier-criteria" style="color: #FF9800;">Participation (50% - 74%)</div>
        <div class="tier-criteria" style="color: #FF9800;">Engagement (50% - 74%)</div> 
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <p class="tier3-text">Tier 3 Students</p>
        <div class="tier-criteria" style="color: #EF5350;">Responsiveness to Surveys (&lt;50%)</div>
        <div class="tier-criteria" style="color: #EF5350;">Attendance in Sessions (&lt;50%)</div>
        <div class="tier-criteria" style="color: #EF5350;">Participation (&lt;50%)</div> 
        <div class="tier-criteria" style="color: #EF5350;">Engagement (&lt;50%)</div>
        """, unsafe_allow_html=True)

    st.write(' ')
    st.write(' ')

    st.header('Practice Exam Scores')
    st.write('Students were asked to update us with practice exam schedules and scores throughout the program. This is a link to the [Texas JAMP Scholars | MCAT Exam Schedule & Scores Survey](https://forms.gle/pK1bGfvxZZQQvmo26) Here is a [list of responses to the survey as of March 3rd.](https://docs.google.com/spreadsheets/d/1PEhGrf5HiiX70Sb57KZtIPKThSno0o1MFXFJUDvhpuM/edit?usp=sharing) We update the information seen below on a weekly basis.')
    st.write(' ')

    st.dataframe(df_test_scores_student_filtered[['test_name','test_date','actual_exam_score']],use_container_width=True)
    st.write(' ')
    st.write(' ')

    point_exam_scores = alt.Chart(df_test_scores_student_filtered).mark_point().transform_fold(
        fold=['actual_exam_score'],
        as_=['variable','value']
    ).encode(
        x=alt.X(
            'yearmonthdate(test_date):O',
            axis=alt.Axis(
                labelAngle=-45,
                title='Test Date'
            )
        ),
        y=alt.Y(
            'value:Q',
            axis=alt.Axis(
                title='Practice Exam Score'
            ),
            scale=alt.Scale(domain=[470, 528])
        ),
        tooltip=[
            alt.Tooltip('test_date:T', title='Test Date'),
            alt.Tooltip('value:Q', title='Exam Score')
        ],
        color=alt.Color(
            'variable:N',
            legend=alt.Legend(
                title='Exam Scores',
                orient='bottom',
                labelExpr="'Practice Exam Score'"
            )
        )
    )

    st.altair_chart(point_exam_scores,use_container_width=True)
    st.write(' ')
    st.write(' ')

    st.subheader('Practice Exam - Accuracy per Subject')
    st.write(
        'The "Question Topic" column represents the various MCAT subjects tested in the Jack Westin Exams. '
        '"Question Frequency" indicates the number of questions associated with each subject in these exams. '
        '"Student Accuracy" is calculated as the percentage of correctly answered questions for a given subject, '
        'based on the total number of questions attempted.'
    )
    exam_section = st.selectbox("Choose an exam section:", list(df_test_section_scores['Exam Section'].unique()))
    st.dataframe(
        df_test_section_scores_student_filtered[df_test_section_scores_student_filtered['Exam Section'] == exam_section][['Exam Name','Question Topic','Question Frequency','Student Accuracy']].sort_values(by='Exam Name').reset_index(drop=True),
        use_container_width=True)
    st.write(' ')
    st.write(' ')



    st.write(' ')
    st.write(' ')

    st.header('Engagement')
    st.subheader('Self-Learning with Jack Westin Course or Question Bank')
    st.write('This graph displays the number of video lessons or assignments within the Self-Paced JW Complete MCAT Course completed by the student per week')
    st.write(' ')
    st.write(' ')

    line_engagement = alt.Chart(df_engagement_attendance_student_filtered).mark_line(point=True).transform_fold(
            ['completed_lessons'],
            as_=['variable', 'value']
        ).encode(
            x=alt.X(
                'week:O',
                axis=alt.Axis(
                    labelAngle=0,
                    title='Week'
                )
            ),
            y=alt.Y(
                'value:Q',
                axis=alt.Axis(
                    title='Completed Count',
                )
            ),
            tooltip=[
                alt.Tooltip('week:O', title='Week'),
                alt.Tooltip('date_range:N', title='Date Range'),
                alt.Tooltip('value:Q', title='Completed Number of Lessons')
            ],
            color=alt.Color(
                'variable:N',
                legend=alt.Legend(
                    title='Type',
                    orient='bottom',
                    labelExpr="'Completed Course Lessons'"
                )
            )
    )

    st.altair_chart(line_engagement,use_container_width=True)

    st.write(' ')
    st.write(' ')

    st.subheader('Completed Question Sets')
    st.write('This graph displays the number of question sets completed within our question bank per week. Question sets usually range between 5 to 10 questions, and can be discrete or passage-based questions.')
    st.write(' ')
    st.write(' ')

    line_question_sets = alt.Chart(df_engagement_attendance_student_filtered).mark_line(point=True).encode(
        x=alt.X(
            'week:O',
            axis=alt.Axis(
                labelAngle=0,
                title='Week'
            )
        ),
        y=alt.Y(
            'total_completed_passages_discrete_sets',
            axis=alt.Axis(
                title='Completed Number of Question Sets'
            )
        ),
        tooltip=[
            alt.Tooltip('week:O', title='Week'),
            alt.Tooltip('date_range:N', title='Date Range'),
            alt.Tooltip('total_completed_passages_discrete_sets', title='Completed Count')
        ],
    )

    st.altair_chart(line_question_sets,use_container_width=True)

    st.header('Participation')
    st.subheader('Class and Homework Participation')
    st.write(
        '"Class Participation" represents the percentage of class activities students engaged in each week. Here is a [video sample of an in-class activity](https://www.loom.com/share/48b383838811401892a38e17761c4993?sid=3d3e7dc2-b294-4b73-b1c6-8d78e6e0b6e8) a student can participate in. It should also be noted we did not track participation in class polls.\n\n'
        'To note: We encouraged students to utilize resources they have access to, such as AAMC materials, to apply their knowledge. '
        '"Homework Completion" indicates that a student utilized the question sets we provided within our learning platform that reviews material we covered in class.'
    )

    st.write(' ')
    st.write(' ')

    line_participation = alt.Chart(df_engagement_attendance_student_filtered).mark_line(point=True).transform_fold(
        fold=['class_participation', 'homework_participation'], 
        as_=['variable', 'value']
    ).encode(
        x=alt.X(
            'week:O',
            axis=alt.Axis(
                labelAngle=0,
                title='Week'
            )
        ),
        y=alt.Y(
            'value:Q',
            axis=alt.Axis(
                title='Participation Rate',
                format='%'
            )
        ),
        tooltip=[
            alt.Tooltip('week:O', title='Week'),
            alt.Tooltip('date_range:N', title='Date Range'),
            alt.Tooltip('value:Q', title='Participation Rate', format='0.1%')
        ],
        color=alt.Color(
            'variable:N',
            legend=alt.Legend(
                title='Type',
                orient='bottom',
                labelExpr="datum.value == 'class_participation' ? 'Class Participation' : 'Homework Completion'"
            )
        )
    )

    st.altair_chart(line_participation,use_container_width=True)

    st.write(' ')
    st.write(' ')
    st.header('Performance')
    st.subheader('Average Accuracy (%) on Question Sets Per Week')
    st.write(
        'During Session Practice: "In-Class Questions" refer to a student\'s accuracy percentage for question sets specifically given during class. '
        'That being said, these percentages will not be present if a student did not attempt the class activity. Also, to note, a data point will not be present if there was no class during a certain week.\n\n'
        'Self-Learning Practice: "CARS Questions" and "Science Questions" refer to a student\'s weekly performance on independent practice sets that they complete independently. Data points will be present for all weeks the student completed a passage or question set.'
    )
    st.write(' ')
    st.write(' ')

    line_engagement = alt.Chart(df_engagement_attendance_student_filtered).mark_line(point=True).transform_fold(
        fold=['sciences_accuracy', 'cars_accuracy','class_accuracy'], 
        as_=['variable', 'value']
    ).encode(
        x=alt.X(
            'week:O',
            axis=alt.Axis(
                labelAngle=0,
                title='Week'
            )
        ),
        y=alt.Y(
            'value:Q',
            axis=alt.Axis(
                title='Average Accuracy (%)',
                format='%'
            )
        ),
        tooltip=[
            alt.Tooltip('week:O', title='Week'),
            alt.Tooltip('date_range:N', title='Date Range'),
            alt.Tooltip('value:Q', title='Accuracy Rate', format='0.1%')
        ],
        color=alt.Color(
            'variable:N',
            legend=alt.Legend(
                title='Subject',
                orient='bottom',
                labelExpr="datum.value == 'cars_accuracy' ? 'CARS Questions' : datum.value == 'class_accuracy' ? 'In-Class Questions' : 'Science Questions'"
            )
        )
    )

    st.altair_chart(line_engagement,use_container_width=True)

    st.write(' ')
    st.write(' ')
    st.header('Attendance')
    st.write(
        'Below demonstrates the weekly percentage of attendance by students within our "All Student" and "Small Group" classes.\n\n'
        'For example, if there are two large classes and a student attends one of them, they would receive a 50% attendance rate for that week. '
        'A data point with 0% indicates no attendance during that week, while the absence of a data point reflects that no classes were held that week. Here is the [MCAT class schedule for JAMP Scholars](https://drive.google.com/file/d/1ku3YESl2If9v3T-n40lVV-KH1QWRVtOr/view?usp=sharing)'
    )
    st.write(' ')
    st.write(' ')

    line_attendance = alt.Chart(df_engagement_attendance_student_filtered).mark_line(point=True).transform_fold(
        fold=['large_session','small_session'],
        as_=['variable','value']
    ).encode(
        x=alt.X(
            'week:O',
            axis=alt.Axis(
                labelAngle=0,
                title='Week'
            )
        ),
        y=alt.Y(
            'value:Q',
            axis=alt.Axis(
                title='Cumulative Attendance Rate',
                format='%'
            )
        ),
        tooltip=[
            alt.Tooltip('week:O', title='Week'),
            alt.Tooltip('date_range:N', title='Date Range'),
            alt.Tooltip('value:Q', title='Cumulative Attendance Rate', format='0.1%')
        ],
        color=alt.Color(
            'variable:N',
            legend=alt.Legend(
                title='Session Type',
                orient='bottom',
                labelExpr="datum.value == 'large_session' ? 'Classes with All Students' : 'Small Group Sessions'"
            )
        )
    )

    st.altair_chart(line_attendance,use_container_width=True)

with tab2:
    # Create comparison table for retaker cohort
    if not df_retakers.empty:
        # Filter out rows with missing student_id
        df_retakers_clean = df_retakers.dropna(subset=['student_id'])
        
        # Create the comparison table with renamed columns
        comparison_data = []
        
        for _, row in df_retakers_clean.iterrows():
            if pd.notna(row['student_id']):
                comparison_data.append({
                    'Student ID': int(row['student_id']),
                    'Large Group Attendance': f"{row['Large Group Tier Attendance']} → {row['Summer _Large Group Attendance Tier']}" if pd.notna(row['Summer _Large Group Attendance Tier']) else f"{row['Large Group Tier Attendance']} → No Summer Data",
                    'Class Participation': f"{row['Class Participation Tier']} → {row['Summer_ClassParticipation_Tier']}" if pd.notna(row['Summer_ClassParticipation_Tier']) else f"{row['Class Participation Tier']} → No Summer Data",
                    'Small Group Attendance': f"{row['Small Group Tier Attendance']} → {row['Summer_ Small_Group_Attendance_Tier']}" if pd.notna(row['Summer_ Small_Group_Attendance_Tier']) else f"{row['Small Group Tier Attendance']} → No Summer Data",
                    'Survey Tier': f"{row['Survey Tier']} → {row['Summer_SurveyTier']}" if pd.notna(row['Summer_SurveyTier']) else f"{row['Survey Tier']} → No Summer Data"
                })
        
        comparison_df = pd.DataFrame(comparison_data)
        
        # Add explanation text for highlighting
        st.info("💡 **Highlighting Guide**: Cells highlighted in green show students who improved from Tier 3 to Tier 2 or Tier 1, or from Tier 2 to Tier 1 during the summer program. Cells highlighted in red show students who remained at Tier 3 (no improvement).")
        
        # Add column definitions for the tier comparison table
        with st.expander("📋 Column Definitions", expanded=False):
            st.markdown("""
            **📚 Large Group Attendance**  
            Large group classes are focused on content connection, application, and strategy.
            
            **👥 Small Group Attendance**  
            Small groups are focused on learning and studying approach. These sessions are infused with coaching advice from our MCAT experts, leveraging data from thousands of tutored students over the past few years. Topics include 🕒 timing practice exams, 📊 using analytics to rebuild study schedules, 💡 strategy for managing burnout, and other evidence-based methods that drive results.
            
            **📝 Survey Tier**  
            Survey Tiers function as both student engagement tracking and accountability mechanisms.
            
            Retaker cohorts received two separate surveys:
            1️⃣ Exam reporting survey
            2️⃣ Self-reflective survey where students could also indicate their anticipated exam date.
            
            Here is a link to the surveys:
            - **Second Exam Survey**: [https://docs.google.com/forms/d/e/1FAIpQLSe5mRmgeN0WIgCSsrY6SwSD9BjxWolZrjOnI39qr7V3LZUmOQ/viewform?usp=dialog](https://docs.google.com/forms/d/e/1FAIpQLSe5mRmgeN0WIgCSsrY6SwSD9BjxWolZrjOnI39qr7V3LZUmOQ/viewform?usp=dialog)
            - **Exam Reporting Survey**: [https://forms.gle/L74GPWYaW2mhXF4HA](https://forms.gle/L74GPWYaW2mhXF4HA)
            """)
        
        # Add highlighting for students who improved from Tier 3 to Tier 2 or Tier 1, or from Tier 2 to Tier 1, and highlight Tier 3 only in red
        def highlight_improvements(row):
            styles = []
            for col in comparison_df.columns:
                if col == 'Student ID':
                    styles.append('')
                else:
                    # Check if the tier shift shows improvement from Tier 3 to Tier 2 or Tier 1, or from Tier 2 to Tier 1
                    tier_shift = str(row[col])
                    if ('Tier 3 → Tier 2' in tier_shift or 'Tier 3 → Tier 1' in tier_shift or 
                        'Tier 2 → Tier 1' in tier_shift):
                        styles.append('background-color: #90EE90; color: black; font-weight: bold;')
                    elif 'Tier 3 → Tier 3' in tier_shift:
                        styles.append('background-color: #FFB6C1; color: black; font-weight: bold;')
                    else:
                        styles.append('')
            return styles
        
        # Apply the styling
        styled_df = comparison_df.style.apply(highlight_improvements, axis=1)
        st.dataframe(styled_df, use_container_width=True)
        
        # Add summary statistics (removed Total Retaker Students metric)

        st.write(' ')
        st.write(' ')

        # Add Practice Exam Data Table
        st.header('Practice Exam Data')
        st.caption('Practice exam scores and survey completion status for retaker students.')
        
        # Add column definitions
        with st.expander("📋 Column Definitions", expanded=False):
            st.markdown("""
            **Reported Test Date**  
            Represents the test date provided by the student in their survey. If no date was submitted, the column will show "No Date Reported."
            
            **First Attempt**  
            Indicates the score from the student's first official MCAT attempt. If no score information was provided, this column will show "none."
            
            **Practice Exam Survey**  
            Shows whether a student reported at least one practice exam score during the program.
            - "Yes" → Student actively reported practice exam scores.
            - "No" → Student did not report any practice exam scores.
            
            We use this column as both a measure of accountability and engagement.
            
            **Second Attempt**  
            Indicates the score from the student's second official MCAT attempt. If no score information was provided, this column will show "none."
            
            **Difference**  
            Represents the numerical difference between a student's second attempt and first attempt MCAT scores.
            """)
        
        # Create practice exam data table
        practice_exam_data = []
        for _, row in df_retakers_clean.iterrows():
            if pd.notna(row['student_id']):
                first_attempt = row['First Attempt'] if pd.notna(row['First Attempt']) else None
                second_attempt = row['Second Attempt'] if pd.notna(row['Second Attempt']) else None
                difference = row['Difference '] if pd.notna(row['Difference ']) else None

                practice_exam_data.append({
                    'Student ID': int(row['student_id']),
                    'Reported Test Date': row['Reported Test Date'] if pd.notna(row['Reported Test Date']) else 'No Date Reported',
                    'First Attempt': first_attempt,
                    'Practice Exam Survey': row['ExamReport_Survey'] if pd.notna(row['ExamReport_Survey']) else 'No Response',
                    'Second Attempt': second_attempt,
                    'Difference': difference
                })

        practice_exam_df = pd.DataFrame(practice_exam_data)
        st.dataframe(practice_exam_df, use_container_width=True)
