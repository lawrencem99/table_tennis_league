"""Views for Table Tennis Rankings."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from rankings.forms import RegistrationForm
from rankings.models import Game, Group, Player


class BaseLoginMixin(LoginRequiredMixin):
    """Simple mixin to redirect to the correct login page."""

    login_url = reverse_lazy('ranking_login')


class IndexView(TemplateView):
    """Main view for site."""

    template_name = 'rankings/index.html'


class RegisterView(CreateView):
    """Simple Registration view."""

    template_name = 'app/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('ranking_login')


class PlayerView(BaseLoginMixin, TemplateView):
    """View a single player and all it's games."""

    template_name = 'rankings/players/player.html'

    def get_context_data(self, **kwargs):
        context = super(PlayerView, self).get_context_data(**kwargs)

        player_id = self.kwargs.get('pk', None)

        player = get_object_or_404(Player, id=player_id)

        context.update({
            'player': player,
            'groups': player.group_set.all(),
            'active_games': player.games.filter(active=True),
            'completed_games': player.games.filter(active=False),
        })

        return context


class GameView(TemplateView):
    """View for a single game for a given group."""

    template_name = 'rankings/groups/game.html'

    def get_context_data(self, **kwargs):
        context = super(GameView, self).get_context_data(**kwargs)

        group = get_object_or_404(Group, id=self.kwargs.get('group_pk', None))
        game = get_object_or_404(Game, id=self.kwargs.get('game_pk', None))

        context.update({
            'group': group,
            'game': game,
            'players': game.players.order_by('-ranking'),
        })

        return context


class CreateGameView(BaseLoginMixin, CreateView):
    """Create a game for the given group."""

    template_name = 'rankings/groups/create_game.html'
    model = Game
    fields = ['players']

    def form_valid(self, form):
        # Make sure only two players are selected.
        players = form.cleaned_data['players']
        if players.count() != 2:
            form.add_error(
                'players',
                'A game requires two players, please try again.',
            )
            return self.form_invalid(form)

        # Otherwise, connect the game to the group.
        self.object = form.save()
        group = get_object_or_404(Group, id=self.kwargs.get('pk', None))

        group.games.add(self.object)
        group.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(
            'game', 
            kwargs={
                'group_pk': self.kwargs.get('pk', None),
                'game_pk': self.object.pk,
            },
        )


class FinishGameView(BaseLoginMixin, UpdateView):
    """Finish a game for the given group."""

    template_name = 'rankings/groups/edit_game.html'
    model = Game
    fields = [
        'winner',
        'home_score',
        'away_score',
    ]

    def get_form(self):
        """Restrict the choices for the winner field."""
        form = super(FinishGameView, self).get_form()

        game = get_object_or_404(Game, id=self.kwargs.get('pk', None))

        form.fields['winner'].queryset = game.players

        return form

    def form_valid(self, form):
        game = form.save(commit=False)

        if game.active:
            # Only update the game and rankings if it's active.
            
            # Update each player's ranking.
            player_1 = game.players.first()
            player_2 = game.players.last()
            
            Player.update_rankings(
                player=player_1,
                opponent=player_2,
                winner=game.winner,
            )

            # Mark the game as finished.
            game.active = False
            game.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """Redirect back to the game."""

        return reverse_lazy(
            'game', 
            kwargs={
                'group_pk': self.object.group_set.first().pk,
                'game_pk': self.object.pk,
            },
        )


class GroupsView(TemplateView): 
    """View the groups."""

    template_name = 'rankings/groups/groups.html'

    def get_context_data(self, **kwargs):
        context = super(GroupsView, self).get_context_data(**kwargs)

        context['groups'] = Group.objects.all()

        return context


class GroupView(TemplateView):
    """View a single group and all it's players."""

    template_name = 'rankings/groups/group.html'

    def get_context_data(self, **kwargs):
        context = super(GroupView, self).get_context_data(**kwargs)

        group = get_object_or_404(Group, id=self.kwargs.get('pk', None))

        context.update({
            'group': group,
            'players': group.players.order_by('-ranking'),
            'active_games': group.games.filter(active=True),
            'completed_games': group.games.filter(active=False),
        })

        return context


class CreateGroupView(SuccessMessageMixin, CreateView):
    """Simple Create View for adding a new Group."""

    template_name = 'rankings/groups/create_group.html'
    model = Group
    fields = [
        'name',
    ]
    success_url = reverse_lazy('groups')

    def get_success_message(self, cleaned_data):
        name = cleaned_data.get('name')

        return f'{name} was created successfully'


class EditGroupView(BaseLoginMixin, SuccessMessageMixin, UpdateView):
    """Simple EditView for editing a group."""
    
    template_name = 'rankings/groups/edit_group.html'
    model = Group
    fields = [
        'name',
        'players',
    ]

    def get_success_url(self):
        return reverse_lazy('group', kwargs={'pk': self.object.pk})
    
    def get_success_message(self, cleaned_data):
        name = cleaned_data.get('name')

        return f'{name} was edited successfully'
