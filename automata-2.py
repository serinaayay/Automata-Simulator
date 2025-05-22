from collections import defaultdict
import streamlit as st
import graphviz
import time
from PIL import Image


st.set_page_config(layout="wide")

# --- Sidebar for About Section ---
st.sidebar.title("About")
st.sidebar.write("""
This application simulates the following:
    
    • Deterministic Finite 
    Automaton (DFA)
    • Context-Free Grammar (CFG)
    • Pushdown Automaton (PDA)

You can select a language (a and b, or 0 and 1) and enter a string to see how the automaton processes it.

""")

# Add Valid Strings Examples section in sidebar
st.sidebar.markdown("---")
st.sidebar.title("Examples of Valid Strings in each Regular Expression:")

# DFA valid strings
st.sidebar.subheader("Valid Strings")
st.sidebar.info("""
**For a and b language:**
- aabbbabaaabbbbaaaaaaaabbbab
- bbababbbaaabbabbaabbabbabbbab
- aabababababbbbbaaaababaaaaba
- bbababbbbababaabababbbb

**For 0 and 1 language:**
- 10101
- 00110
- 10011
- 11001100
""")

# DFA Invalid strings
st.sidebar.subheader("Invalid Strings")
st.sidebar.info("""
**For a and b language:**
- bbababababbabbabbabbaa
                bbabbababa
- aababbbbababaabbaaab
                babbaabbabbabbabab
- bbbbbabab
- aababababbbababbbbb

**For 0 and 1 language:**
- 10101
- 00110
- 10011
- 11001100
                
    </style>    
""")

st.sidebar.write("You may use the simulation buttons to see step-by-step processing of your input strings.")

st.title("Automata Theory and Formal Languages Simulator")

# Tabs hehe
dfa_tab, cfg_tab, pda_tab = st.tabs(["DFA", "CFG", "PDA"])

with dfa_tab:
    st.header("Deterministic Finite Automaton (DFA)")

    # --- DFA class ---
    class DFA:
        def __init__(self, states, alphabet, transition_function, start_state, accept_states):
            self.states = states
            self.alphabet = alphabet
            self.transition_function = transition_function
            self.start_state = start_state
            self.accept_states = accept_states

        def accepts(self, input_string):
            current_state = self.start_state
            for symbol in input_string:
                if symbol not in self.alphabet:
                    return False  # invalid symbol
                current_state = self.transition_function.get((current_state, symbol))
                if current_state is None:
                    return False  # no valid transition
            return current_state in self.accept_states
        

    def simulate_dfa(dfa, input_string):
        """Simulate DFA step-by-step and collect transitions."""
        current_state = dfa.start_state
        path = [(current_state, None)]  # list of (state, symbol)

        for symbol in input_string:
            if symbol not in dfa.alphabet:
                return path, False, f"Invalid symbol '{symbol}'"
            
            next_state = dfa.transition_function.get((current_state, symbol))
            if next_state is None:
                return path, False, f"No transition from {current_state} on '{symbol}'"

            # Debug output
            print(f"Current State: {current_state}, Input Symbol: '{symbol}', Next State: {next_state}")

            path.append((next_state, symbol))
            current_state = next_state

        # Continue simulation even if we end in a trap state
        accepted = current_state in dfa.accept_states
        return path, accepted, None
        
    def draw_dfa(dfa, active_state=None):
        dot = graphviz.Digraph()
        dot.attr(rankdir='LR', size="14,8")

        # Draw nodes
        for state in dfa.states:
            if state in dfa.accept_states:
                if state == active_state:
                    dot.node(state, shape="doublecircle", style="filled", color="lightgreen")
                else:
                    dot.node(state, shape="doublecircle")
            else:
                if state == active_state:
                    dot.node(state, style="filled", color="lightgreen")
                else:
                    dot.node(state)

        # Start arrow
        dot.node("start", shape="none", label="")
        dot.edge("start", dfa.start_state)

        # Group transitions with same (from_state, to_state)
        edge_labels = defaultdict(list)
        for (from_state, symbol), to_state in dfa.transition_function.items():
            edge_labels[(from_state, to_state)].append(symbol)

        for (from_state, to_state), symbols in edge_labels.items():
            label = ', '.join(sorted(symbols))
            dot.edge(from_state, to_state, label=label)

        return dot

    def draw_input_pointer(input_string, position):
        """Draw input string with a moving pointer ^."""
        spaced_input = '  '.join(input_string)
        pointer = '   ' * position + '^'
        return spaced_input + "\n" + pointer


    # --- DFA definition based on image ---
    states = {
        '0', '1', '2','3','4','5','6','7','8','9','10','11','12','13',
        '14','15','16','17','18','19','20', '21', '22', 'T1', 'T2'  # Add trap states explicitly
    }
    alphabet = {'a', 'b', '0', '1'}

    # Make sure all transitions to trap states are properly defined
    transition_function_ab = {
        ('0', 'b'): '1',
        ('0', 'a'): '2',
        ('1', 'b'): '2',
        ('1', 'a'): 'T1',  # Trap state T1
        ('2', 'b'): 'T1',  # Trap state T1
        ('T1', 'a'): 'T1', # Self-loop on trap state
        ('T1', 'b'): 'T1', # Self-loop on trap state
        ('2', 'a'): '1',
        ('1', 'b'): '3',
        ('2', 'a'): '3',
        ('3', 'b'): '5',
        ('3', 'a'): '4',
        ('4', 'b'): '6',
        ('4', 'a'): 'T2',  # Trap state T2
        ('T2', 'a'): 'T2', # Self-loop on trap state
        ('T2', 'b'): 'T2', # Self-loop on trap state
        ('5', 'a'): '7',
        ('5', 'b'): '8',
        ('6', 'a'): '9',
        ('6', 'b'): 'T2',  # Trap state T2
        ('7', 'b'): '9',
        ('8', 'b'): '9',
        ('8', 'a'): 'T2',  # Trap state T2
        ('9', 'a'): '10',
        ('9', 'b'): '11',
        ('10', 'a'): '12',
        ('10', 'b'): '11',
        ('11', 'b'): '12',    
        ('11', 'a'): '10',   
        ('12', 'b'): '13',
        ('13', 'b'): '12',
        ('13', 'a'): '10',
        ('12', 'a'): '14',
        ('14', 'b'): '14', 
        ('14', 'a'): '15', 
        ('15', 'b'): '15', 
        ('15', 'a'): '16', 
        ('16', 'b'): '18', 
        ('16', 'a'): '17',
        ('17', 'a'): '18',
        ('17', 'b'): '16',
        ('18', 'a'): '19',
        ('18', 'b'): '16', 
        ('16', 'b'): '20',
        ('20', 'b'): '21',
        ('20', 'a'): '16', 
        ('21', 'b'): '22',
        ('21', 'a'): '16',
        ('22', 'b'): '22',  
        ('22', 'a'): '22',  
        ('19', 'a'): '19', 
        ('19', 'b'): '19', 
 
    }

    transition_function_01 = {
        ('0', '1'): '0',
        ('0', '0'): '1',
        ('1', '1 '): '1',
        ('1', '0'): '2',
        ('2', '1'): '2',
        ('2', '0'): '3',
        ('2', '1'): '4',
        ('3', '0'): '5',
        ('4', '1'): '5',
        ('4', '0'): 'T',
        ('3', '1'): 'T',
        ('5', '0'): '6',
        ('5', '1'): '6',
        ('6', '0'): '7',
        ('6', '1'): '8',
        ('7', '0'): '9',
        ('8', '1'): '10',
        ('9', '0'): '11',
        ('10', '1'): '11',
        ('11', '1'): '12',
        ('11', '0'): '13',
        ('12', '1'): '14',
        ('15', '0'): '13', #Return
        ('15', '1'): '16', 
        ('13', '0'): '15', #Destination
        ('13', '1'): '14',
        ('14', '0'): '14',
        ('14', '1'): '16', 
        ('16', '0'): '16',
        ('16', '1'): '17',
        ('17', '1'): '18',
        ('17', '0'): '17',
        ('18', '1'): '19',
        ('18', '0'): '20',
        ('19', '1'): '18',
        ('20', '0'): '18',
        ('20', '1'): '22',
        ('19', '0'): '21',
        ('21', '1'): '21',
        ('21', '0'): '21',
        ('22', '1'): '22',
        ('22', '0'): '22',

    }
    start_state = '0'
    accept_states = {'19', '22'}

    option = st.selectbox(
        "Select a language",
        ("a and b", "0 and 1"),
        key="dfa_language",
        placeholder="Select Language...",
    )


    # --- Visualization ---
    st.subheader("DFA Diagram")

    # Initialize DFAs based on selected language
    if option == "a and b":
        dfa = DFA(states, {'a', 'b'}, transition_function_ab, start_state, accept_states)
        st.graphviz_chart(draw_dfa(dfa), use_container_width=True)

        st.subheader("Regular Expression for a and b")
        st.write("(aa+bb) (aba+bab+bbb) (a+b)* (aa+bb) (aa+bb)* (ab* ab* a) (ab* ab* a)* (bbb+aaa) (a+b)*")
        
        # input fields for testing
        st.subheader("Test Strings")
        
        # Process each input field 
        for idx in range(5):
            key = f"input{idx+1}_ab"
            test_input = st.text_input("Enter a string:", key=key)
            
            if test_input:
                path, accepted, error = simulate_dfa(dfa, test_input)
                
                # Apply CSS styling based on result
                if error or not accepted:
                    # Red for rejected or error
                    st.markdown(f"""
                    <style>
                    div[data-testid="stTextInput"] input[aria-label="Enter a string:"][value="{test_input}"] {{
                        background-color: rgba(255, 0, 0, 0.2);
                        border-color: red;
                    }}
                    </style>
                    """, unsafe_allow_html=True)
                else:
                    # Green for accepted
                    st.markdown(f"""
                    <style>
                    div[data-testid="stTextInput"] input[aria-label="Enter a string:"][value="{test_input}"] {{
                        background-color: rgba(0, 255, 0, 0.2);
                        border-color: green;
                    }}
                    </style>
                    """, unsafe_allow_html=True)
                
                # simulation button
                sim_key = f"sim_button_{idx+1}_ab"
                if st.button(f"Simulate DFA for input {idx+1}", key=sim_key):
                    if error:
                        st.error(f"Error: {error}")
                    else:
                        st.write("### Step-by-Step DFA Simulation:")

                        stop_button = st.button("Stop Simulation", key=f"stop_sim_{idx+1}_ab")
                        
                        placeholder = st.empty()  # for the DFA diagram
                        input_placeholder = st.empty()  # for the input string and pointer
                        
                        for step_idx, (state, symbol) in enumerate(path):
                            # Check if stop button was pressed
                            if st.session_state.get(f"stop_sim_{idx+1}_ab", False):
                                st.warning("Simulation stopped by user.")
                                break
                                
                            with placeholder.container():
                                st.graphviz_chart(draw_dfa(dfa, active_state=state))
                            
                            # show input string with moving pointer
                            with input_placeholder.container():
                                if step_idx == 0:
                                    input_pos = 0
                                else:
                                    input_pos = step_idx - 1  # because path has an extra initial start state
                                st.code(draw_input_pointer(test_input, input_pos), language="markdown")
                                
                                if step_idx == 0:
                                    st.write(f"Start at state **{state}**")
                                else:
                                    st.write(f"Read **'{symbol}'**, move to state **{state}**")
                            
                            # Add a small delay between steps
                            time.sleep(0.9)
                        
                        # Show final result if simulation completed
                        if not st.session_state.get(f"stop_sim_{idx+1}_ab", False):
                            if accepted:
                                st.success(f"The string '{test_input}' is **ACCEPTED** by the DFA! 🎉")
                            else:
                                st.error(f"The string '{test_input}' is **REJECTED** by the DFA. ❌")
                                
        
    elif option == "0 and 1":
        dfa = DFA(states, {'0', '1'}, transition_function_01, start_state, accept_states)
        st.graphviz_chart(draw_dfa(dfa), use_container_width=True)

        st.subheader("Regular Expression for 0 and 1")
        st.write("(1* 01* 01*) (11+00) (10+01)* (1+0) (11+00) (1+0+11+00+101+111+000) (11+00)* (10* 10* 1) (11+00)*")
        
        # Multiple input fields for testing
        st.subheader("Test Strings")
        
        # Process each input field with custom styling
        for idx in range(5):
            key = f"input{idx+1}_01"
            test_input = st.text_input("Enter a string:", key=key)
            
            if test_input:
                path, accepted, error = simulate_dfa(dfa, test_input)
                
                # Apply CSS styling based on result
                if error or not accepted:
                    # Red for rejected or error
                    st.markdown(f"""
                    <style>
                    div[data-testid="stTextInput"] input[aria-label="Enter a string:"][value="{test_input}"] {{
                        background-color: rgba(255, 0, 0, 0.2);
                        border-color: red;
                    }}
                    </style>
                    """, unsafe_allow_html=True)
                else:
                    # Green for accepted
                    st.markdown(f"""
                    <style>
                    div[data-testid="stTextInput"] input[aria-label="Enter a string:"][value="{test_input}"] {{
                        background-color: rgba(0, 255, 0, 0.2);
                        border-color: green;
                    }}
                    </style>
                    """, unsafe_allow_html=True)
                
                # Add simulation button
                sim_key = f"sim_button_{idx+1}_01"
                if st.button(f"Simulate DFA for input {idx+1}", key=sim_key):
                    if error:
                        st.error(f"Error: {error}")
                    else:
                        st.write("### Step-by-Step DFA Simulation:")
                        
                        # Create a stop button
                        stop_button = st.button("Stop Simulation", key=f"stop_sim_{idx+1}_01")
                        
                        placeholder = st.empty()  # for the DFA diagram
                        input_placeholder = st.empty()  # for the input string and pointer
                        
                        for step_idx, (state, symbol) in enumerate(path):
                            # Check if stop button was pressed
                            if st.session_state.get(f"stop_sim_{idx+1}_01", False):
                                st.warning("Simulation stopped by user.")
                                break
                                
                            with placeholder.container():
                                st.graphviz_chart(draw_dfa(dfa, active_state=state))
                            
                            # show input string with moving pointer
                            with input_placeholder.container():
                                if step_idx == 0:
                                    input_pos = 0
                                else:
                                    input_pos = step_idx - 1  # because path has an extra initial start state
                                st.code(draw_input_pointer(test_input, input_pos), language="markdown")
                                
                                if step_idx == 0:
                                    st.write(f"Start at state **{state}**")
                                else:
                                    st.write(f"Read **'{symbol}'**, move to state **{state}**")
                            
                            # Add a small delay between steps
                            time.sleep(0.5)
                        
                        # Show final result if simulation completed
                        if not st.session_state.get(f"stop_sim_{idx+1}_01", False):
                            if accepted:
                                st.success(f"The string '{test_input}' is **ACCEPTED** by the DFA! 🎉")
                            else:
                                st.error(f"The string '{test_input}' is **REJECTED** by the DFA. ❌")
                                
                        # Add a "Return to Testing" button
                        if st.button("Return to Testing", key=f"return_{idx+1}_01"):
                            # This button doesn't need to do anything - clicking it will rerun the app
                            pass
    else:
        dfa = None
        input_string = None
        st.write("Please select a language to see the DFA diagram.")

with cfg_tab:
    st.header("Context-Free Grammar (CFG)")

    cfg = st.selectbox(
        "Select a language",
        ["a and b", "0 and 1"],
        key="cfg_language",
        placeholder="Select Language...",
    )

    #cfg for a and b
    if cfg == "a and b":
        st.subheader("CFG for a and b")
        try:
            cfg_image = Image.open("CFG 1 FINAL.png")
            st.image(cfg_image, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading CFG image: {e}")

        st.subheader("Regular Expression for a and b")
        st.write("(aa+bb) (aba+bab+bbb) (a+b)* (aa+bb) (aa+bb)* (ab* ab* a) (ab* ab* a)* (bbb+aaa) (a+b)*")

    #cfg for 0 and 1
    elif cfg == "0 and 1":

        st.subheader("CFG for 0 and 1")
        try:
            cfg_image = Image.open("A AND B PDA.png")
            st.image(cfg_image, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading CFG image: {e}")

        st.subheader("Regular Expression for a and b")
        st.write("(1* 01* 01*) (11+00) (10+01)* (1+0) (11+00) (1+0+11+00+101+111+000) (11+00)* (10* 10* 1) (11+00)*")



with pda_tab:
    st.header("Pushdown Automaton (PDA)")

    pda = st.selectbox(
        "Select a language",
        ["a and b", "0 and 1"],
        placeholder="Select Language...",
        key="pda_language_selector"
    )


    if pda == "a and b":
        st.subheader("PDA for a and b")
        try:
            pda_image = Image.open("PDA 1 FINAL.png")
            st.image(pda_image, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading CFG image: {e}")

        st.subheader("Regular Expression for a and b")
        st.write("(aa+bb) (aba+bab+bbb) (a+b)* (aa+bb) (aa+bb)* (ab* ab* a) (ab* ab* a)* (bbb+aaa) (a+b)*")


    elif pda == "0 and 1":
        st.subheader("PDA for 0 and 1")
        try:
            cfg_image = Image.open("PDA 2 FINAL.png")
            st.image(cfg_image, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading CFG image: {e}")

        st.subheader("Regular Expression for 0 and 1")
        st.write("(1* 01* 01*) (11+00) (10+01)* (1+0) (11+00) (1+0+11+00+101+111+000) (11+00)* (10* 10* 1) (11+00)*")

