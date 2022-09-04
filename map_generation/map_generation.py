'''
Inputs:
*   Map
  * x,y plot
*   Robot Path Pose
  * Pose contains x,y,room
* List of all the rooms in the environemnt
  * List of str
Output:
* Map with labeled room
'''
def extractAndLabelPoses(map, rooms, path):
  with open('/content/drive/MyDrive/Colab Notebooks/data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
          line_count += 1
        else:
          quat_rotx = row[8]
          quat_roty = row[9]
          quat_rotz = row[10]
          quat_rotw = row[11]

          w = float(quat_rotw)
          x = -float(quat_rotz)
          y = float(quat_rotx)
          z = -float(quat_roty)

          yaw   =  m.atan2(2.0 * (w*z + x*y), w*w + x*x - y*y - z*z) * 180.0 / m.pi;

          path.append([x,y])

          line_count += 1

'''
Inputs:
*   Map
  * x,y plot
*   Robot Path Pose
  * Pose contains x,y,room
* List of all the rooms in the environemnt
  * List of str
Output:
* Map with labeled room
'''
def filterPoses(map, rooms, path):

  # Size of window filter
  window_size = 10

  # Counter that moves the window along the path
  path_idx = 1

  for pose in path:
    # Setup a dictionnary to keep track of the occurance of each room within the filter
    room_occ = {}

    # Initialize the dictionnary to contain all of the found rooms
    for room in rooms:
      room_occ.update({room: 0})

    # Running total of the coordinates in the window. Used to find the centroid coordinate of the window
    rc_x = 0
    rc_y = 0

    # Scan over the window
    for i in range(window_size):

      # Add to the running total of the coordinates in the window. Used to find the centroid coordinate of the window
      rc_x = rc_x + path[path_idx + i][0]
      rc_y = rc_y + path[path_idx + i][1]

      # Used to determine the room type with the highest occurence in the window
      max_w = 0
      in_room = ""

      # Scan over every room. Used to compare each individual pose to the known rooms
      for room in rooms:

        # Current room is the same as in the pose
        if (room == path[path_idx + i][2]):
          # Increment the counter in the dicitionnary for that specific room
          room_occ.update({room: room_occ[room]+1})
        
        # Update the room with the highest occurance
        if (room_occ[room]/window_size > max_w):
          max_w = room_occ[room]/window_size
          in_room = room
      
    # Take the average of the running total of coordinates. This is the centroid of the room
    room_cord_x = rc_x / window_size
    room_cord_y = rc_y / window_size
    
    # Move the window along
    if (path_idx < len(path)/2):
      path_idx = path_idx + 1
    else:
      break

    print("coordinate x,y: " + str(room_cord_x) + " " + str(room_cord_y) + " is in room " + in_room)