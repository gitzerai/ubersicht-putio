command: "python my.widget/putio.widget/get-data.py"

# the refresh frequency in milliseconds
refreshFrequency: 1000 * 60 * 60

render: -> """
  <h1>Put.io (<span class='from-date'></span> - <span class='to-date'></span>)</h1>
  <table></table>
  <p class='message'></p>
"""

update: (output, domEl) ->
  @$domEl = $(domEl)
  @renderTable output

renderTable: (data) ->
  $table = @$domEl.find('table')
  $table.html("""<thead>
               <tr>
                 <th>Name</th>
                 <th>Season</th>
                 <th>Episode</th>
               </tr>
              </thead>
              <tbody></tbody>
              <tfooter></tfooter>
  """)
  $tableBody = $table.find('tbody')

  for key, value of JSON.parse data
    if key == 'error' || key == 'message'
      @renderMessage(value)
    else if key == 'from_date'
      $date = @$domEl.find('.from-date')
      $date.html(value)
    else if key == 'to_date'
      $date = @$domEl.find('.to-date')
      $date.html(value)
    else
      $tableBody.append @renderRow(key, value)

renderMessage: (message) ->
  $message = @$domEl.find('.message')
  $message.html """#{message}"""

renderRow: (key, value) ->
  return """<tr>
              <td><a href='#{value.link}'>#{value.name}</a></td>
              <td>#{value.season}</td>
              <td>#{value.episode}</td>
            </tr>"""

style: """
  color: #FFFFFF
  font-family: Helvetica Neue
  right: 20px
  bottom: 20px
  min-width: 350px
  max-width: 500px

  table
    margin-top: 16px
    width: 100%
    text-align: right

  table thead tr th
    padding-bottom: 8px
    border-bottom: 1px dashed white
    opacity: 0.5

  table tbody tr:first-child td
    padding-top: 8px

  table th:first-child, table td:first-child
    text-align left

  .message
    opacity: 0.5
    text-align: right

  a
    color: white
    text-decoration: none

  h1
    font-size: 2em
    font-weight: 100
    text-align: right
    margin: 0
    padding: 0

"""
