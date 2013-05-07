# smploxy

Local proxy for sending links from browser to SMPlayer.

Mainly this proxy intended to work with https://github.com/RushOnline/chrome-sendlink

## Example

Usage example (find all links contains 'mp3' and add 'play' button):

```javascript
  $('a[href*=mp3]').each(function() {
    return $(this).before($('<button href="#"></button>').addClass('btn btn-small icon-play').data('href', this.href).click(function() {
      var request;

      request = {
        type: "POST",
        url: 'http://localhost:8001/',
        crossDomain: true,
        data: {
          command: 'playlist.add',
          item: $(this).data('href')
        },
        success: function(response) {
          return console.debug(response);
        },
        error: function(response) {
          console.debug(response);
          return alert('Use SMPlayer with local proxy: https://github.com/RushOnline/smploxy');
        }
      };
      return $.ajax(request);
    }));
  });
```
## TODO

- Use SMPlayer connection success/failure in response to browser
- Autodetect SMPlayer remote management port from config (temp/autoport in ~/.config/smplayer/smplayer.ini)
