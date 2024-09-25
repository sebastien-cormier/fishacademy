import streamlit as st
import matplotlib.pyplot as plt

from include.next_session import get_next_session, get_next_session_name, reset_next_session
from include.new_session import save_shopping, save_recave, save_chips_return, delete_draft_csv, load_draft_csv, backup_draft_csv
from include.utils import to_euro
from include.es_client import get_es_client
from include.es_queries import index_game_session, get_sessions

es_client = get_es_client()

def valid_game_session(_df_session) :
    if round(float(df_session.amount.sum()),2)==0.0 :
        index_game_session(es_client, _df_session)
        backup_draft_csv(_df_session)
        delete_draft_csv()
        reset_next_session()
        return True
    else :
        return False
    

next_session = get_next_session()

if next_session is None :
    st.markdown(f"Veuillez créer la session avant de la lancer.")

else :
    
    if 'setting_ok' not in st.session_state:
        st.session_state['setting_ok'] = False
    if 'session_name' not in st.session_state:
        st.session_state['session_name'] = get_next_session_name(get_sessions(es_client))
    if 'initial_bank_amount' not in st.session_state:
        st.session_state['initial_bank_amount'] = 300
    if 'current_bank_amount' not in st.session_state:
        st.session_state['current_bank_amount'] = 300
    if 'food_amount' not in st.session_state:
        st.session_state['food_amount'] = 10.0
        
    list_player = next_session['coming']
    list_player.append(next_session['host'])

    if 'list_total_chips' not in st.session_state:
        st.session_state['list_total_chips'] = [0] * len(list_player)
    if 'list_pie_explode' not in st.session_state:
        st.session_state['list_pie_explode'] = [0] * len(list_player)  # 0.1 to explode value for player
    list_total_chips = st.session_state['list_total_chips']
    list_pie_explode = st.session_state['list_pie_explode']

    if not st.session_state['setting_ok'] :
        df_ = load_draft_csv()
        if df_ is not None :
            # Reload state from CSV
            st.session_state['df_session'] = df_
            st.session_state['setting_ok'] = True
            st.session_state['session_name'] = df_['session'].iloc[0]
            st.session_state['food_amount'] = -df_.loc[df_.tx_type=='REPAS']['amount'].iloc[0]
            for index, row in df_.loc[df_.tx_type=='BUY_CHIPS'].iterrows() :
                p_index = list_player.index(row.player)
                list_total_chips[p_index] = list_total_chips[p_index] - row.amount
                st.session_state['list_total_chips'] = list_total_chips
                st.session_state['current_bank_amount'] = st.session_state['current_bank_amount'] + row.amount
            for index, row in df_.loc[df_.tx_type=='SELL_CHIPS'].iterrows() :
                st.session_state['current_bank_amount'] = st.session_state['current_bank_amount'] + row.amount

    diff_bank_amount = st.session_state['current_bank_amount'] - st.session_state['initial_bank_amount']

    st.markdown(f"# {st.session_state['session_name']}")
    st.markdown(f"__Liste des joueurs inscrits :__ "+", ".join(list_player) + ".")


    if not st.session_state['setting_ok'] :

        st.caption("La partie n'a pas été démarrée. Veuillez sélectionner les paramètres pour la lancer.")

        
        with st.expander("Paramètres", expanded = True):

            with st.form("game_settings"):
                new_session_name = st.text_input("Identifiant session", st.session_state['session_name'])
                shopping_user = st.selectbox("Qui a fait les courses ?",list_player)
                contribution = st.slider("Participation demandée (€)", 0.0, 20.0, 10.0,  0.1)
                bank_amount = st.slider("Montant en banque (€) ?", 100, 500, st.session_state['initial_bank_amount'], 10)
                submit = st.form_submit_button('Enregistrer')
                if submit:
                    #df_c = save_shopping(new_session_name, shopping_user, list_player, contribution)
                    st.session_state['setting_ok'] = True
                    st.session_state['session_name'] = new_session_name
                    st.session_state['food_amount'] = contribution
                    st.session_state['initial_bank_amount'] = bank_amount
                    st.session_state['current_bank_amount'] = bank_amount
                    st.session_state['df_session'] = save_shopping(new_session_name, shopping_user, list_player, contribution)
                    st.rerun()

    else :

        df_session = st.session_state['df_session'].sort_values("@timestamp", ascending=False)

        if st.session_state['setting_ok'] :
            with st.sidebar.form("recave", clear_on_submit=True):
                player_recave = st.selectbox("Ajouter une cave", [*["Joueur"], *list_player])
                amount_recave = st.slider("Montant de la recave (€) ?", 0.0, 10.0, 10.0,  0.05)
                submit = st.form_submit_button('Ajouter')
                if submit:
                    if player_recave == "Joueur" :
                        st.warning("Choisir un joueur")
                    else :
                        df_session = save_recave(df_session, st.session_state['session_name'], player_recave, amount_recave)
                        p_index = list_player.index(player_recave)
                        list_total_chips[p_index] = list_total_chips[p_index] + amount_recave
                        st.session_state['df_session'] = df_session
                        st.session_state['current_bank_amount'] = st.session_state['current_bank_amount'] - amount_recave
                        st.rerun()

            with st.sidebar.form("chips_return", clear_on_submit=True):
                player_return = st.selectbox("Retour jetons", [*["Joueur"], *list_player])
                amount_return = st.slider("Montant retourné (€) ?", 0.05, round(float(-diff_bank_amount),2), 10.0,  0.05)
                submit = st.form_submit_button('Enregistrer')
                if submit:
                    if player_return == "Joueur" :
                        st.warning("Choisir un joueur")
                    else :
                        df_session = save_chips_return(df_session, st.session_state['session_name'], player_return, amount_return)
                        st.session_state['current_bank_amount'] = st.session_state['current_bank_amount'] + amount_return
                        st.session_state['df_session'] = df_session
                        st.rerun()

        #st.sidebar.markdown(f"Debug:")
        #st.sidebar.markdown(f" - setting_ok : __{st.session_state['setting_ok']}__")
        #st.sidebar.markdown(f" - session_name: __{st.session_state['session_name']}__")
        #st.sidebar.markdown(f" - initial_bank_amount: __{st.session_state['initial_bank_amount']}__")
        #st.sidebar.markdown(f" - current_bank_amount: __{st.session_state['current_bank_amount']}__")
        #st.sidebar.markdown(f" - list player: __{list_player}__")
        #st.sidebar.markdown(f" - list chips: __{list_total_chips}__")


        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Nombre de joueurs", len(list_player))
        col2.metric("Participation repas", to_euro(st.session_state['food_amount']))
        
        total_recave = -diff_bank_amount - len(list_player)*10
        if total_recave < 0 :
            total_recave = 0
        col3.metric("Argent sur la table", to_euro(-diff_bank_amount), to_euro(total_recave))
        col4.metric("Jetons en banque", to_euro(st.session_state['current_bank_amount']), to_euro(diff_bank_amount))

        
        if sum(list_total_chips)>20 :
            st.divider()
            # Pie chart, where the slices will be ordered and plotted counter-clockwise:
            st.markdown("## Contribution au montant global")
            fig1, ax1 = plt.subplots()
            ax1.pie(list_total_chips, explode=list_pie_explode, labels=list_player, autopct='%1.1f%%',
                    shadow=True, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig1)

        st.divider()
        st.markdown("## Dernières transactions de la session")
        st.dataframe(df_session.set_index(df_session.columns[0]))

        st.divider()
        col1, col2 = st.columns(2)
        if col1.button(":no_entry: Réinitialiser la session", type="secondary") :
            delete_draft_csv()
            st.toast(":no_entry: Draft supprimé !")
            st.rerun()
            
        if col2.button(":white_check_mark: Valider la session", type="primary") :
            if valid_game_session(df_session) :
                st.toast(f":white_check_mark: Session valide, comptes mis à jours dans l'index.")

            else :
                st.toast(f":warning: Session invalide, il y a une différence de  {round(df_session.amount.sum(),2)} €.")
