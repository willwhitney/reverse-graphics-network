#iGeoNice to iGeo matrix
import theano
import theano.tensor as T
theano.config.exception_verbosity = 'high'
import pdb,math
import numpy as np

def getINTMMatrix(bsize, rng, igeon_pose):
	intensity = igeon_pose[0]
	t0=igeon_pose[:,1]; t1=igeon_pose[:,2]
	s0=igeon_pose[:,3]; s1=igeon_pose[:,4]
	z=igeon_pose[:,5];
	# cos_theta=T.cos(igeon_pose[:,6]); sin_theta=T.sin(igeon_pose[:,6])
	theta = igeon_pose[:, 6]

	image_size = 10.
	# offset = np.array([-image_size / 2, -image_size / 2, 1])
	offset = T.ones([bsize, 3, 1])
	offset = T.set_subtensor(offset[:,0,0], T.constant(image_size / 2))
	offset = T.set_subtensor(offset[:,1,0], T.constant(image_size / 2))

	# rotation = np.array([[math.cos(theta), -math.sin(theta), 0],
 #                     [math.sin(theta),  math.cos(theta), 0],
 #                     [0,0,1]])
	# counterrotation = np.array([[math.cos(-theta), -math.sin(-theta), 0],
	#                      [math.sin(-theta),  math.cos(-theta), 0],
	#                      [0,0,1]])

	# counterrotated_offset = np.dot(counterrotation, np.array([offset_x, offset_y, 1]))

	# recentering = np.array([[1,0,counterrotated_offset[0]],
	#                         [0,1,counterrotated_offset[1]],
	#                         [0,0,1]])


	# pdb.set_trace()

	# np_fix_centr_to_origin = np.array([[1,0,-0.5],[0,1,-0.5],[0,0,1]])
	# fix_center_to_origin = theano.shared(value=np_fix_centr_to_origin, name='np_fix_centr_to_origin', borrow=True)
	fix_center_to_origin = T.zeros([bsize, 3, 3])
	fix_center_to_origin = T.set_subtensor(fix_center_to_origin[:,0,0], T.constant(1.0))
	fix_center_to_origin = T.set_subtensor(fix_center_to_origin[:,0,2], -offset[0, 0, 0])
	fix_center_to_origin = T.set_subtensor(fix_center_to_origin[:,1,1], T.constant(1.0))
	fix_center_to_origin = T.set_subtensor(fix_center_to_origin[:,1,2], -offset[0, 1, 0])
	fix_center_to_origin = T.set_subtensor(fix_center_to_origin[:,2,2], T.constant(1.0))


	# np_trans_matrix = numpy.array([[1,0,t0],[0,1,t1],[0,0,1]])
	trans_matrix = T.zeros([bsize, 3 , 3])
	trans_matrix = T.set_subtensor(trans_matrix[:,0,0], T.constant(1.0))
	trans_matrix = T.set_subtensor(trans_matrix[:,1,1], T.constant(1.0))
	trans_matrix = T.set_subtensor(trans_matrix[:,2,2], T.constant(1.0))

	trans_matrix = T.set_subtensor(trans_matrix[:,0,2], t0)
	trans_matrix = T.set_subtensor(trans_matrix[:,1,2], t1)

	# np_scaling_matrix = numpy.array([[s0,1,1],[0,s1,1],[0,0,1]])
	# scaling_matrix = theano.shared(value=np_scaling_matrix, name='np_scaling_matrix', borrow=True)
	scaling_matrix = T.zeros([bsize,3,3])
	scaling_matrix = T.set_subtensor(scaling_matrix[:,0,0], s0)
	scaling_matrix = T.set_subtensor(scaling_matrix[:,1,1], s1)
	# scaling_matrix = T.set_subtensor(scaling_matrix[:,1,2], T.constant(1.0)) ##
	scaling_matrix = T.set_subtensor(scaling_matrix[:,2,2], T.constant(1.0))


	# np_shearing_matrix = numpy.array([[1,z,0],[0,1,1],[0,0,1]])
	# shearing_matrix = theano.shared(value=np_shearing_matrix, name='np_shearing_matrix', borrow=True)
	shearing_matrix = T.zeros([bsize,3 ,3])
	shearing_matrix = T.set_subtensor(shearing_matrix[:,0,1], z)
	shearing_matrix = T.set_subtensor(shearing_matrix[:,0,0], T.constant(1.0))
	shearing_matrix = T.set_subtensor(shearing_matrix[:,1,1], T.constant(1.0))
	# shearing_matrix = T.set_subtensor(shearing_matrix[:,1,2], T.constant(1.0)) ##
	shearing_matrix = T.set_subtensor(shearing_matrix[:,2,2], T.constant(1.0))


	# np_rot_matrix = numpy.array([[cos_theta, -sin_theta, 0],[sin_theta,cos_theta,1],[0,0,1]])
	# rot_matrix = theano.shared(value=np_rot_matrix, name='np_rot_matrix', borrow=True)
	rot_matrix = T.zeros([bsize,3,3])
	# rot_matrix = T.set_subtensor(rot_matrix[:,1,2], T.constant(1.0)) ##
	rot_matrix = T.set_subtensor(rot_matrix[:,2,2], T.constant(1.0))
	rot_matrix = T.set_subtensor(rot_matrix[:,0,0], T.cos(theta))
	rot_matrix = T.set_subtensor(rot_matrix[:,0,1], -T.sin(theta))
	rot_matrix = T.set_subtensor(rot_matrix[:,1,0], T.sin(theta))
	rot_matrix = T.set_subtensor(rot_matrix[:,1,1], T.cos(theta))

	counter_rot_matrix = T.zeros([bsize,3,3])
	# counter_rot_matrix = T.set_subtensor(counter_rot_matrix[:,1,2], T.constant(1.0)) ##
	counter_rot_matrix = T.set_subtensor(counter_rot_matrix[:,2,2], T.constant(1.0))
	counter_rot_matrix = T.set_subtensor(counter_rot_matrix[:,0,0], T.cos(-theta))
	counter_rot_matrix = T.set_subtensor(counter_rot_matrix[:,0,1], -T.sin(-theta))
	counter_rot_matrix = T.set_subtensor(counter_rot_matrix[:,1,0], T.sin(-theta))
	counter_rot_matrix = T.set_subtensor(counter_rot_matrix[:,1,1], T.cos(-theta))

	counterrotated_offset = T.batched_dot(counter_rot_matrix, offset)
	# pdb.set_trace()

	# np_fix_corner_to_origin = np.array([[1,0,0.5],[0,1,0.5],[0,0,1]])
	# fix_corner_to_origin = theano.shared(value=np_fix_corner_to_origin, name='np_fix_corner_to_origin', borrow=True)
	fix_corner_to_origin = T.zeros([bsize, 3, 3])
	fix_corner_to_origin = T.set_subtensor(fix_corner_to_origin[:,0,0], T.constant(1.0))
	fix_corner_to_origin = T.set_subtensor(fix_corner_to_origin[:,0,2], counterrotated_offset[0,0,0])
	fix_corner_to_origin = T.set_subtensor(fix_corner_to_origin[:,1,1], T.constant(1.0))
	fix_corner_to_origin = T.set_subtensor(fix_corner_to_origin[:,1,2], counterrotated_offset[0,1,0])
	fix_corner_to_origin = T.set_subtensor(fix_corner_to_origin[:,2,2], T.constant(1.0))
	igeo_pose = T.batched_dot(fix_center_to_origin, T.batched_dot(trans_matrix, T.batched_dot(scaling_matrix, T.batched_dot(shearing_matrix, T.batched_dot(rot_matrix, fix_corner_to_origin)))))
	# igeo_pose = T.batched_dot(fix_corner_to_origin, T.batched_dot(rot_matrix, T.batched_dot(shearing_matrix, T.batched_dot(scaling_matrix, T.batched_dot(trans_matrix, fix_center_to_origin)))))
	n1 = fix_center_to_origin.eval()[0];
	n2 = trans_matrix.eval()[0];
	n3 = scaling_matrix.eval()[0];
	n4 = shearing_matrix.eval()[0];
	n5 = rot_matrix.eval()[0];
	n6 = fix_corner_to_origin.eval()[0];
	npres = np.dot(n1,np.dot(n2,np.dot(n3,np.dot(n4, np.dot(n5,n6)))))
	# igeo_pose = fix_center_to_origin * trans_matrix * scaling_matrix * shearing_matrix * rot_matrix * fix_corner_to_origin
	pdb.set_trace()
	return igeo_pose



