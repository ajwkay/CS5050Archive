document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#submit-button').addEventListener('click', send_all_mail);

  if (!localStorage.getItem('sesh')) {
  // By default, load the inbox
    load_mailbox('inbox');
  }
  else {
    load_mailbox('sent');
    localStorage.removeItem('sesh');
  }
});

function tester() {
  console.log('Click!');
}


function load(page) {
  fetch(`/emails/${page}`)
  .then(response => response.json())
  .then(emails => {
      emails.forEach(add_mail);
  });
};

// Add a new mail with given contents to DOM
function add_mail(contents) {

    // Create new post
    const mail = document.createElement('button');
    if (contents.read) {
      mail.className = 'read-mail';
    }
    else {
      mail.className = 'unread-mail';
    }
    mail.innerHTML = `<b>${contents.subject}</b>, from <i>${contents.sender}</i> at <i>${contents.timestamp}</i>`;
    mail.onclick = function() {
      view_email(contents.id);
    };

    // Add post to DOM
    document.querySelector('#emails-view').append(mail);
};

function send_all_mail() {

  //Extract recipients list separated by commas and/or spaces.
  let recipient_list = document.querySelector('#compose-recipients').value.split(/(?:,| )+/)

  //Send to each recipient.
  recipient_list.forEach(send_mail_loop);

  //Load Sent mailbox.
  localStorage.setItem('sesh', true);
}

function send_mail_loop(recipient) {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipient,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value,
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });
}

function reply_email(id) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#read-view').style.display = 'none';

  //Fill fields with original mail contents
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#compose-recipients').value = email.sender;
    if (email.subject.toLowerCase().indexOf('re:') === 0) {
      document.querySelector('#compose-subject').value = email.subject;
    }
    else {
      document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    }
    document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}` ;
    });
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#read-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function view_email(id) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#read-view').style.display = 'block';

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {

    //Read the mail
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    })

    //Fill the page with mail contents
    document.querySelector('#subject').innerHTML = email.subject;
    document.querySelector('#sender').innerHTML = email.sender;
    let list = '';
    console.log(list);
    email.recipients.forEach((recipient) => {
      list = list.concat(recipient);
    });
    document.querySelector('#recipients').innerHTML = list;
    document.querySelector('#body').innerHTML = email.body;
    document.querySelector('#timestamp').innerHTML = email.timestamp;

    //Functionalise Buttons
    document.querySelector('#reply').onclick = () => reply_email(id);
    if (email.archived) {
      document.querySelector('#archive').style.display = 'none';
      document.querySelector('#unarchive').style.display = 'inline-block';
    }
    else {
      document.querySelector('#archive').style.display = 'inline-block';
      document.querySelector('#unarchive').style.display = 'none';
    }
    document.querySelector('#archive').onclick = () => archive_email(id);
    document.querySelector('#unarchive').onclick = () => archive_email(id);
  });
};

function archive_email(id) {
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      if (email.archived) {
        document.querySelector('#archive').style.display = 'inline-block';
        document.querySelector('#unarchive').style.display = 'none';
        fetch(`/emails/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: false
          })
        })
      }
      else {
        document.querySelector('#archive').style.display = 'none';
        document.querySelector('#unarchive').style.display = 'inline-block';
        fetch(`/emails/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: true
          })
        })
      }
  });
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#read-view').style.display = 'none';

  //Load the mail
  load(mailbox);

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}
