function Use() {
  const cardData = [
    {
      step: 1,
      heading: "Upload Presentation",
      desc: "Click on Start editing, then tap the Record button to turn your presentation into a video you can convert to save PPT as MP4. Flixier’s  PowerPoint recorder works like a charm to record your decks.",
    },
    {
      step: 2,
      heading: "Edit and Enhance",
      desc: "Experiment with video and audio customization features before you convert your PowerPoint to MP4. Go for snappy transitions, colorful effects,  information in your presentation.",
    },
    {
      step: 3,
      heading: "Convert and Save",
      desc: "Click on the Export button and make sure you select Video from the Format dropdown options. Flixier does its magic almost instantly and automatically produces your requested MP4 file.",
    },
  ];
  return (
    <div className="use">
      <h2 className="use-heading">How to convert PowerPoint to MP4?</h2>
      <div className="cards">
        {cardData.map((data, i) => (
          <div className="card" key={i}>
            <div className="circle">{data.step}</div>
            <div className="card-head">{data.heading}</div>
            <div className="desc">{data.desc}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
export default Use;
