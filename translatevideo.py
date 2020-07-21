
import argparse
from transcribeUtils import *
from srtUtils import *
import time
from videoUtils import *
from audioUtils import *



# Get the command line arguments and parse them
parser = argparse.ArgumentParser( prog='translatevideo.py', description='Process a video found in the input file, process it, and write tit out to the output file')
parser.add_argument('-region', required=True, help="The AWS region containing the S3 buckets" )
parser.add_argument('-inbucket', required=True, help='The S3 bucket containing the input file')
parser.add_argument('-infile', required=True, help='The input file to process')
parser.add_argument('-outbucket', required=True, help='The S3 bucket containing the input file')
parser.add_argument('-outfilename', required=True, help='The file name without the extension')
parser.add_argument('-outfiletype', required=True, help='The output file type.  E.g. mp4, mov')
parser.add_argument('-outlang', required=True, nargs='+', help='The language codes for the desired output.  E.g. en = English, de = German')		
args = parser.parse_args()

# print out parameters and key header information for the user
print( "==> translatevideo.py:\n")
print( "==> Parameters: ")
print("\tInput bucket/object: " + args.inbucket + args.infile)
print( "\tOutput bucket/object: " + args.outbucket + args.outfilename + "." + args.outfiletype)

print( "\n==> Target Language Translation Output: " )

for lang in args.outlang:
	print( "\t" + args.outbucket + args.outfilename + "-" + lang + "." + args.outfiletype)
	
	
# Create Transcription Job
response = createTranscribeJob( args.region, args.inbucket, args.infile )

# loop until the job successfully completes
print( "\n==> Transcription Job: " + response["TranscriptionJob"]["TranscriptionJobName"] + "\n\tIn Progress"),

while( response["TranscriptionJob"]["TranscriptionJobStatus"] == "IN_PROGRESS"):
	print( "."),
	time.sleep( 30 )
	response = getTranscriptionJobStatus(response["TranscriptionJob"]["TranscriptionJobName"])

print( "\nJob Complete")
print( "\tStart Time: " + str(response["TranscriptionJob"]["CreationTime"]) )
print( "\tEnd Time: "  + str(response["TranscriptionJob"]["CompletionTime"]) )
print( "\tTranscript URI: " + str(response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]) )

# Now get the transcript JSON from AWS Transcribe
transcript = getTranscript( str(response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]) ) 
# print( "\n==> Transcript: \n" + transcript)

# Create the SRT File for the original transcript and write it out.  
writeTranscriptToSRT( transcript, 'en', "subtitles-en.srt" )  
createVideo( args.infile, "subtitles-en.srt", args.outfilename + "-en." + args.outfiletype, "audio-en.mp3", True)


# Now write out the translation to the transcript for each of the target languages
for lang in args.outlang:
	writeTranslationToSRT(transcript, 'en', lang, "subtitles-" + lang + ".srt", args.region ) 	
	
	#Now that we have the subtitle files, let's create the audio track
	createAudioTrackFromTranslation( args.region, transcript, 'en', lang, "audio-" + lang + ".mp3" )
	
	# Finally, create the composited video
	createVideo( args.infile, "subtitles-" + lang + ".srt", args.outfilename + "-" + lang + "." + args.outfiletype, "audio-" + lang + ".mp3", False)
	
	


	
