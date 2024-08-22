import { stub, restore, assert, match } from 'sinon';

describe('uploadAudio function', () => {
  let mockFetch;
  let audioBlob;

  beforeEach(() => {
    mockFetch = stub(window, 'fetch');
    audioBlob = new Blob(); // Assuming you have a way to create a test audio blob
  });

  afterEach(() => {
    restore();
  });

  it('should upload audio blob to /upload_audio endpoint', async () => {
    const expectedResponse = { message: 'File uploaded successfully' };
    mockFetch.resolves(new Response(JSON.stringify(expectedResponse), { status: 200 }));

    await uploadAudio(audioBlob);

    // Assert that fetch was called with correct parameters
    assert.calledOnceWithExactly(mockFetch, '/upload_audio', {
      method: 'POST',
      body: match((body) => body instanceof FormData && body.get('audio') === audioBlob),
    });
  });

  it('should handle errors during upload', async () => {
    const error = new Error('Network Error');
    mockFetch.rejects(error);

    try {
      await uploadAudio(audioBlob);
      fail('Expected error during upload');
    } catch (err) {
      expect(err).toEqual(error); // Assert the caught error
    }
  });
});