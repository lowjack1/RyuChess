"use strict";

window.onload = init();

function init() {
    startGame('board1');
    startGame('board2');
    updateLeaderBoardTable();
}


function startGame(chess_board_id) {
    var board = null;
    var game = new Chess();

    function onDragStart (source, piece, position, orientation) {
        // do not pick up pieces if the game is over
        if (game.game_over()) return false
      
        // only pick up pieces for the side to move
        if ((game.turn() === 'w' && piece.search(/^b/) !== -1) || (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
            return false
        }
    }

    function onDrop (source, target) {

        // see if the move is legal
        var move = game.move({
            from: source,
            to: target,
            promotion: 'q' // NOTE: always promote to a queen for example simplicity
        });
      
        // illegal move
        if (move === null) return 'snapback'
    }

    function onSnapEnd () {
        board.position(game.fen())
    }

    function makeRandomMove () {
        var possibleMoves = game.moves()
      
        // exit if the game is over
        if (game.game_over()) return
      
        var randomIdx = Math.floor(Math.random() * possibleMoves.length)
        game.move(possibleMoves[randomIdx])
        board.position(game.fen())
      
        window.setTimeout(makeRandomMove, 500)
    }
 
    var config = {
        pieceTheme: "/static/images/chesspieces/wikipedia/{piece}.png",
        dropOffBoard: 'snapback',
        draggable: true,
        position: 'start',
        onDragStart: onDragStart,
        onDrop: onDrop,
        onSnapEnd: onSnapEnd
    };
    board = Chessboard(chess_board_id, config);
    
    // window.setTimeout(makeRandomMove, 500);
}


// ########################################################################################


function updateLeaderBoardTable() {
    let table_data = [
        {
            name: 'lowjack',
            total_games: 10,
            game_won: 10
        },
        {
            name: 'fastboot',
            total_games: 10,
            game_won: 9
        },
        {
            name: 'starboy_jb',
            total_games: 10,
            game_won: 8
        },
        {
            name: 'masterbios',
            total_games: 10,
            game_won: 7
        },
        {
            name: 'ikusab',
            total_games: 10,
            game_won: 6
        },
        {
            name: 'unam',
            total_games: 10,
            game_won: 5
        },
        {
            name: 'masterbios',
            total_games: 10,
            game_won: 7
        },
        {
            name: 'ikusab',
            total_games: 10,
            game_won: 6
        },
        {
            name: 'unam',
            total_games: 10,
            game_won: 5
        },
        {
            name: 'ikusab',
            total_games: 10,
            game_won: 6
        }
    ];

    let html = "";
    $.each(table_data, function(idx, data) {
        let rank_html = idx + 1;
        if(idx == 0) {
            rank_html = `<i class="fa fa-trophy fa-lg" style="color:#FFDF00">`;
        } else if(idx == 1) {
            rank_html = `<i class="fa fa-trophy fa-lg" style="color:#C0C0C0">`;
        } else if(idx == 2) {
            rank_html = `<i class="fa fa-trophy fa-lg" style="color:#cd7f32">`;
        } else {
            rank_html = `<span style="color: #4D5656"><strong>${idx+1}</strong></span>`
        }

        html += `
            <tr>
                <td class="text-center">${rank_html}</td>
                <td>
                    <div class="media">
                        <img class="mr-3" src="/static/images/sonic.jpg" style="width: 3.1em"/>
                        <div class="media-body">
                            <h5 class="leaderboard-username">${data['name']}</h5>
                            <span class="small text-muted"><i class="flag-icon flag-icon-in mr-2"></i>International master</span>
                        </div>
                    </div>
                </td>
                <td>
                    <span class="pr-2" style="color: green"><i class="fa fa-play win-icon"></i> ${data['game_won']}</span> 
                    <span>-</span>
                    <span class="pl-2" style="color:red"><i class="fa fa-play lose-icon"></i> ${data['total_games']}</span></td>
            </tr>`;
    });

    html = `
        <table class="table table-borderless">
            <tbody>
                ${html}
            </tbody>
        </table>`;

    $('#leaderboard_card .leaderboard_table').html(html);
}


// #####################################################################################################

$('button[name="play_friend_btn"').on('click', searchFriendDropdown);

function searchFriendDropdown() {
    $('button[name="play_friend_btn"').hide();
    
    // bootstrap-select2-theme is not responsive, just to fix the issue set width parameter to null
    $.fn.select2.defaults.set("width", null);
    $('select[name="user_friend_dropdown"]').select2({
        'theme': 'bootstrap',
        placeholder: function(){
            $(this).data('placeholder');
        }
    })
    $('select[name="user_friend_dropdown"]').fadeIn(400);
}