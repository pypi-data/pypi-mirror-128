"""
Simple CBS account class with method to add study seat/room bookings to calendar.
Can be run as command line
"""

class CBSaccount:
	def __init__(self, username, password):
		from exchangelib import Credentials, Configuration, Account, EWSTimeZone, DELEGATE
		
		username = username
		password = password
		mailAddress = username + '@student.cbs.dk'
		credentials = Credentials(mailAddress, password)
		
		config = Configuration(credentials = credentials,
		                       server = 'outlook.office365.com')
		self.account = Account(primary_smtp_address = mailAddress,
		                       access_type = DELEGATE,
		                       autodiscover = False,
		                       credentials = credentials,
		                       config = config)
		self.tz = EWSTimeZone('Europe/Copenhagen')

	
	def updateCalendar(self):
		from exchangelib import CalendarItem, EWSDateTime
		import datetime as dt
		
		today = dt.datetime.today().replace(tzinfo=self.tz)
		twoWeeksAgo = today-dt.timedelta(days=15)
		
		# all mails with booking confirmation sent during the last two weeks
		bookingMails = self.account.inbox.filter(f'From:lokaleadm@cbs.dk, '
		                                         f'Sent:{twoWeeksAgo.strftime("%m/%d/%Y")}'
		                                         f'..{today.strftime("%m/%d/%Y")}')
		
		seatQuota = 0
		seatQuotaNext = 0
		roomQuota = 0
		roomQuotaNext = 0
		updatedBookings = []
		if bookingMails.count() == 0: # see if there are any mails from the last 15 days
			print('Found no booking mails (from the last 2 weeks) to add to calendar.')
		else: # add bookings to calendar
			for mail in bookingMails[::-1]:
				confirmation = mail.subject.startswith('Booking Confirmation')
				cancellation = mail.subject.startswith('Booking Cancellation')
				
				if not any([confirmation, cancellation]): # only relevant mails, otherwise go to next iteration
					continue
				
				indAdd = 0
				stringAdj = 0
				if cancellation:
					indAdd = 1
					stringAdj = -5
				
				groupRoom = "This booking was for a 'Group Study Room'" in mail.body.splitlines()[8+indAdd]
				studySeat = "This booking was for a 'Single Study Seat'" in mail.body.splitlines()[8+indAdd]
				
				if groupRoom:
					seatString = 'Group Room: ' + mail.body.splitlines()[4+indAdd].strip()[11+stringAdj:]
					seatRoomLocation = seatString[6:]
				elif studySeat:
					seatString = 'Seat: ' + mail.body.splitlines()[4+indAdd].strip()[11+stringAdj:-13]
					seatRoomLocation = seatString[6:]
				else:
					seatString = mail.body.splitlines()[4+indAdd].strip()
					seatRoomLocation = seatString[11+stringAdj:]
				
				dayString, monthString, yearString = mail.body.splitlines()[5+indAdd].strip().split()[2].split(sep='-')
				timeStartString, timeEndString = mail.body.splitlines()[6+indAdd].strip().split()[1].split(sep='-')
				
				hourStart = int(timeStartString.split(sep=':')[0])
				minuteStart = int(timeStartString.split(sep=':')[1])
				
				hourEnd = int(timeEndString.split(sep=':')[0])
				minuteEnd = int(timeEndString.split(sep=':')[1])
				
				startdt = dt.datetime(**{'year':int(yearString),
				                         'month':int(monthString),
				                         'day':int(dayString),
				                         'hour':hourStart,
				                         'minute':minuteStart}).replace(tzinfo = self.tz)
				enddt = dt.datetime(**{'year':int(yearString),
				                       'month':int(monthString),
				                       'day':int(dayString),
				                       'hour':hourEnd,
				                       'minute':minuteEnd}).replace(tzinfo = self.tz)
				
				# if booking is in the past, go to next iteration
				yesterday = today - dt.timedelta(days=1)
				if startdt < yesterday:
					continue
				
				startEWS = EWSDateTime.from_datetime(startdt)
				endEWS = EWSDateTime.from_datetime(enddt)
				
				# skip duplicates
				alreadyThere = self.account.calendar.filter(**{'subject':seatString,
				                                               'start':startEWS,
				                                               'end':endEWS,
				                                               'location':seatRoomLocation}).all().count() != 0
				sentThisWeek = mail.datetime_sent.isocalendar().week == mail.datetime_sent.today().isocalendar().week
				
				if alreadyThere:
					if all([alreadyThere, cancellation]):
						self.account.calendar.filter(**{'subject':seatString,
						                                'start':startEWS,
						                                'end':endEWS,
						                                'location':seatRoomLocation})[0].delete()
						
						# check if quota update is from this week
						if sentThisWeek:
							if groupRoom:
								roomQuota = int(mail.body.splitlines()[13].strip().split()[2])
								roomQuotaNext = int(mail.body.splitlines()[14].strip().split()[2])
							elif studySeat:
								seatQuota = int(mail.body.splitlines()[13].strip().split()[2])
								seatQuotaNext = int(mail.body.splitlines()[14].strip().split()[2])
						
						updateString = [f'    {seatString}.  '
						                f'Time: {startEWS.strftime("%H:%M")}-{endEWS.strftime("%H:%M")}.  '
						                f'Date: {startEWS.strftime("%d/%m/%Y")}']
						if updateString[0] in updatedBookings:
							updatedBookings[updatedBookings.index(updateString[0])] = updateString[0] + '  (CANCELLED)'
						else:
							updatedBookings.append(updateString[0] + '  (CANCELLED)')
				else:
					ev = CalendarItem(folder=self.account.calendar,
					                  subject=seatString,
					                  start=startEWS,
					                  end=endEWS,
					                  location=seatRoomLocation)
					ev.save()
					
					# check if quota update is from this week
					if sentThisWeek:
						if groupRoom:
							roomQuota = int(mail.body.splitlines()[12].strip().split()[2])
							roomQuotaNext = int(mail.body.splitlines()[13].strip().split()[2])
						elif studySeat:
							seatQuota = int(mail.body.splitlines()[12].strip().split()[2])
							seatQuotaNext = int(mail.body.splitlines()[13].strip().split()[2])
					
					updatedBookings.append(f'    {seatString}.  '
					                       f'Time: {startEWS.strftime("%H:%M")}-{endEWS.strftime("%H:%M")}.  '
					                       f'Date: {startEWS.strftime("%d/%m/%Y")}')
			
			if len(updatedBookings) != 0:
				if not all([seatQuota==0, seatQuotaNext==0,
				            roomQuota==0, roomQuotaNext==0]):
					updatedBookings.append(f'\nStudy seat quota this week: {seatQuota}/40,    Next week: {seatQuotaNext}/40'
					                       f'\nGroup room quota this week: {roomQuota}/10,    Next week: {roomQuotaNext}/10')
				print('Study seats and/or group room bookings added to calendar:')
				print('\n'.join(updatedBookings))
			elif len(updatedBookings) == 0:
				print('Found no new relevant bookings to add to calendar.')




