"use client";
import { UserContext } from "@/app/layout.tsx";
import axios from "axios";
import { ChangeEvent, useContext, useState } from "react";
import "./styles.css";

const CreateLesson = ({ params }: { params: { sectionId: string } }) => {
	const { token } = useContext(UserContext)!;
	const [title, setTitle] = useState("");
	const [type, setType] = useState("video");
	const [videoLink, setVideoLink] = useState("");

	const [selectedFile, setSelectedFile] = useState<File | null>(null);

	const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
		const file = event.target.files?.[0];
		if (!file) return;
		setSelectedFile(file);
	};

	const handleSubmit = async () => {
		try {
			if (type === "video" && !videoLink) return;
			if (type === "pdf" && !selectedFile) return;

			const videoOrPdf =
				type === "video"
					? { video_url: videoLink }
					: { pdf: selectedFile };

			await axios.post(
				`http://0.0.0.0:8080/app/courses/create_lesson`,
				{ title, section: params.sectionId, type, ...videoOrPdf },
				{
					headers: {
						Authorization: `Token ${token}`,
					},
				}
			);
		} catch {
			// todo: Laith implement the toast
		}
	};

	return (
		<div className="form-style-8">
			<h2>Create your own lesson</h2>
			<form action="">
				<label htmlFor="title">Course name:</label>
				<input
					id="title"
					type="text"
					name="title"
					placeholder="The best course"
					value={title}
					onChange={(e) => setTitle(e.target.value)}
				/>
				
				<label htmlFor="options">Lesson type:</label>
				<select
					id="options"
					value={type}
					onChange={(e) => setType(e.target.value)}
				>
					<option value="video">Video</option>
					<option value="pdf">PDF file</option>
				</select>

				{type === "pdf" ? (
					<>
						<label htmlFor="pdfFile">Select a PDF file:</label>
						<input
							type="file"
							id="pdfFile"
							accept=".pdf"
							onChange={handleFileChange}
						/>
					</>
				) : (
					<>
						<label htmlFor="videoLink">Type the video link:</label>
						<input
							id="videoLink"
							type="url"
							name="link"
							placeholder="video link"
							value={videoLink}
							onChange={(e) => setVideoLink(e.target.value)}
						/>
					</>
				)}

				<input
					type="button"
					value="Upload your lesson!"
					onClick={() => handleSubmit()}
				/>
			</form>
		</div>
	);
};

export default CreateLesson;